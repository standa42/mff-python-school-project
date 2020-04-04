
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

    def float_x_to_window_units(self, x):
        return x * self.size[0]

    def float_y_to_window_units(self, y):
        return y * self.size[1]

    def float_to_window_units(self, x, y):
        return (self.float_x_to_window_units(x), self.float_y_to_window_units(y))



class GameScreen(Screen):
    def on_pre_enter(self):
        game_widget = self.ids.game_widget
        game_widget.clear()
        # initGame

    def on_leave(self):
        game_widget = self.ids.game_widget
        game_widget.clear()
        self.ball.canvas.clear()
        self.remove_widget(self.ball)

    def on_enter(self):
        game_widget = self.ids.game_widget
        with self.canvas.before:
            Color(0, 0, 0.7)
        game_widget.createMap()

        tank = TankWidget()
        tank.build()
        self.add_widget(tank)

        self.ball = BallWidget()
        self.ball.build()
        self.add_widget(self.ball)
        kivy.clock.Clock.schedule_interval(self.update, 1/30)

    def update(self, dt):
        self.ball.update(dt)



class TanksApp(App):
    pass

if __name__ == '__main__':
    TanksApp().run()