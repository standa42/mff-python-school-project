
import kivy
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from random import random
from kivy.graphics import Color, Ellipse, Line, Rectangle

from pathlib import Path
import os

from kivy.graphics import Mesh
from functools import partial
from math import cos, sin, pi

from statistics import mean
from HallOfFame import HallOfFameScreen
from Menu import MenuScreen

import numpy as np

import kivy.clock

# Bans resize
# from kivy.config import Config
# Config.set('graphics', 'resizable', False)

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter((self.x, self.y))

class BallWidget(Widget):
    def build(self):
        self.pos = [400, 400]
        with self.canvas:
            Color(0.2, 0.5, 0.5)
            Ellipse(pos=self.pos, size=(20, 20), segments = 30)
    
    def update(self, dt):
        self.canvas.clear()
        self.pos[0] -= 1
        with self.canvas:
            Color(0.2, 0.5, 0.5)
            Ellipse(pos=self.pos, size=(20, 20), segments = 30)

class TankWidget(Widget):
    def build(self):
        with self.canvas:
            Color(1, 0.2, 0)
            Ellipse(pos=(300, 300), size=(20, 20), angle_start = -90, angle_end = 90, segments = 30)
            Ellipse(pos=(307, 320), size=(5, 5), segments = 30)


class MapWidget(Widget):
    map_segments_count = 300
    map_edge_tank_padding = 25
    min_tank_mutual_distance = 30

    def clear(self):
        self.canvas.clear()

    def generate_terrain(self):
        self.scene = self.parent.parent
        self._generate_surface()
        self._regenerate_mesh()     

    def generate_tanks_positions(self, number_of_tanks):
        map_edge_padding = 25
        required_distance = 30
        positions = []

        for _ in range(number_of_tanks):
            while True:
                # generate random position and check whether it is distant enought from all other
                position = random.randint(MapWidget.map_edge_tank_padding, MapWidget.map_segments_count - MapWidget.map_edge_tank_padding)
                if all(map(lambda other_position: abs(position - other_position), positions)):
                    break
            positions.append(self._position_index_to_float(position), self.surface)



    def _generate_surface(self):
        self.surface = []
        self.surface_x = []
        self.surface_y = []

        # initial (left) point of surface
        surface_height = random() * 0.4 + 0.3 # (0.3 - 0.7)
        # controls slope (height change) to the next terrain segment
        steepness = 0

        for i in range(MapWidget.map_segments_count):
            # revert steepness if it is too high/low
            if surface_height > 0.8 or surface_height < 0.2:
                steepness *= -0.1
            # add random noise
            steepness += np.random.normal() / 2000
            # steer direction towards the middle
            steepness += (0.5 - surface_height) / 500
            # clip (for lower hills)
            steepness = np.clip(steepness, -0.005, 0.005)

            surface_height = surface_height + steepness
            x = self._position_index_to_float(i)

            self.surface.append(Point(x, surface_height))
            self.surface_x.append(x)
            self.surface_y.append(surface_height)

    def _regenerate_mesh(self):
        vertices = []
        indices = []

        scene = self.scene

        for i in range(MapWidget.map_segments_count):
            float_x, float_y = self.surface[i]
            x = scene.float_x_to_window_units(float_x)
            y = scene.float_y_to_window_units(float_y)
            # surface point
            vertices.extend([int(x), int(y), 0, 0])

            x = scene.float_x_to_window_units(float_x)
            y = scene.float_y_to_window_units(0)
            # map bottom point
            vertices.extend([int(x), int(0), 0, 0])

        # corners to make it polygonal fill of widget under surface
        vertices.extend([scene.float_x_to_window_units(1), scene.float_y_to_window_units(random()), 0, 0])
        vertices.extend([scene.float_x_to_window_units(1), scene.float_y_to_window_units(0), 0, 0])
        vertices.extend([scene.float_x_to_window_units(1), scene.float_y_to_window_units(0), 0, 0])
        vertices.extend([scene.float_x_to_window_units(0), scene.float_y_to_window_units(0), 0, 0])

        indices = list(range(MapWidget.map_segments_count*2 + 4))

        with self.canvas.before:
            # blue sky
            Color(0.4, 0.9, 1)
            Rectangle(pos=(0,0), size=self.size)
        with self.canvas:
            # green terrain
            Color(0.2, 0.85, 0.3)
            self.mesh = Mesh(vertices=vertices, indices=indices, mode='triangle_strip') 

    def _position_index_to_float(self, index):
        return index / (MapWidget.map_segments_count - 1)

class GameWidget(Widget):
    def on_touch_down(self, touch):
        color = (random(), random(), random())
        with self.canvas:
            Color(*color)
            d = 30.
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

    def clear(self):
        self.canvas.clear()

    def createMap(self):
        wid = self
        with wid.canvas.before:
            Color(0.4, 0.9, 1)
            Rectangle(pos=(0,0), size=self.size)
        with wid.canvas:
            Color(0.2, 0.85, 0.3)
            self.mesh = self.build_mesh()

    def build_mesh(self):
        """ returns a Mesh of a rough circle. """
        print(str(self.size))

        vertices = []
        indices = []

        segments = 300
        
        last_y = random() * 0.4 + 0.3
        steepness = 0
        
        for i in range(segments):
            steepness += (np.random.normal() / 2000) + (0.5 - last_y) / 500 
            steepness = np.clip(steepness, -0.005, 0.005)

            new_y = last_y + steepness
            last_y = new_y

            if new_y > 0.8 or new_y < 0.2:
                steepness *= -0.1

            x = self.float_x_to_window_units(float(i) / segments)
            y = self.float_y_to_window_units(new_y)
            vertices.extend([int(x), int(y), 20, 60])

            x = self.float_x_to_window_units(float(i) / segments)
            y = self.float_y_to_window_units(0)
            vertices.extend([int(x), int(y), 200, 200])

        vertices.extend([self.float_x_to_window_units(1), self.float_y_to_window_units(random()), 0, 0])
        vertices.extend([self.float_x_to_window_units(1), self.float_y_to_window_units(0), 0, 0])
        vertices.extend([self.float_x_to_window_units(1), self.float_y_to_window_units(0), 0, 0])
        vertices.extend([self.float_x_to_window_units(0), self.float_y_to_window_units(0), 0, 0])

        indices = list(range(segments*2 + 4))
        return Mesh(vertices=vertices, indices=indices, mode='triangle_strip') # triangle_fan
        # ('points', 'line_strip', 'line_loop', 'lines',
        #         'triangle_strip', 'triangle_fan'):

    



class GameScreen(Screen):
    def on_pre_enter(self):
        map_widget = self.ids.map_widget
        map_widget.clear()
        # initGame

    def on_leave(self):
        map_widget = self.ids.map_widget
        map_widget.clear()
        # self.ball.canvas.clear()
        # self.remove_widget(self.ball)

    def on_enter(self):
        map_widget = self.ids.map_widget
        map_widget.generate_terrain()

        # tank = TankWidget()
        # tank.build()
        # self.add_widget(tank)

        # self.ball = BallWidget()
        # self.ball.build()
        # self.add_widget(self.ball)
        # kivy.clock.Clock.schedule_interval(self.update, 1/30)

    def update(self, dt):
        self.ball.update(dt)

    def float_x_to_window_units(self, x):
        return x * self.size[0]

    def float_y_to_window_units(self, y):
        return y * self.size[1]

    def float_to_window_units(self, x, y):
        return (self.float_x_to_window_units(x), self.float_y_to_window_units(y))



class TanksApp(App):
    pass

if __name__ == '__main__':
    TanksApp().run()