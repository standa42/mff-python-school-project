
import kivy
from kivy.app import App
from kivy.lang import Builder

from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from random import random, randint
from kivy.graphics import Color, Ellipse, Line, Rectangle

from pathlib import Path
import os

from kivy.graphics import Mesh
from functools import partial
from math import cos, sin, pi

from statistics import mean
from HallOfFame import HallOfFameScreen
from Menu import MenuScreen
from Map import MapWidget
from Point import Point

import numpy as np

import kivy.clock

from kivy.graphics import Rotate
from kivy.graphics.context_instructions import PopMatrix, PushMatrix


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
    tank_size = 26
    tank_barrel_size = Point(4,6)

    def build(self, player_number, color, position):
        self.player_number = player_number
        self.color = color
        self.position = position

        self.barrel_rotation = 0

        self.draw()
        

    def draw(self):
        with self.canvas:
            Color(self.color.r, self.color.g, self.color.b)
            # half-circle
            Ellipse(pos=(self.position.x - TankWidget.tank_size/2, self.position.y - TankWidget.tank_size/2), size=(TankWidget.tank_size, TankWidget.tank_size), angle_start = -90, angle_end = 90, segments = 30)
            # base
            Rectangle(pos=(self.position.x - TankWidget.tank_size/2, self.position.y - TankWidget.tank_size/4), size=(TankWidget.tank_size, TankWidget.tank_size/4))
            # barrel
            PushMatrix()
            self.rot = Rotate()
            self.rot.angle = self.barrel_rotation
            self.rot.origin = (self.position.x, self.position.y)
            Rectangle(pos=(self.position.x - TankWidget.tank_barrel_size.x/2, self.position.y), size=(TankWidget.tank_barrel_size.x, TankWidget.tank_size/2 + TankWidget.tank_barrel_size.y))
            PopMatrix()


class GameScreen(Screen):
    colors = [
        Color(0.933, 0.090, 0.117), # Red
        Color(0.090, 0.368, 0.933), # Blue
        Color(0.933, 0.090, 0.878), # Purple
        Color(0.941, 0.627, 0.141), # Orange
        Color(0.3, 0.5, 0.2), # Dark green
        Color(0, 0, 0 )  # Black
    ]

    def set_scene(self, number_of_players, screen_size):
        self.number_of_players = number_of_players
        self.screen_size = Point(screen_size[0], screen_size[1])

    def on_pre_enter(self):
        map_widget = self.ids.map_widget
        map_widget.clear()
        map_widget.generate_terrain()
        tanks_positions = map_widget.generate_tanks_positions(self.number_of_players)

        self.tanks = []
        for i in range(self.number_of_players):
            tank = TankWidget()
            tank.build(i, GameScreen.colors[i], tanks_positions[i])
            self.add_widget(tank)
            self.tanks.append(tank)


    def on_leave(self):
        self.ids.map_widget.clear()
        for tank in self.tanks:
            self.remove_widget(tank)

    def on_enter(self):
        
        pass
        # tank = TankWidget()
        # tank.build()
        # self.add_widget(tank)

        # self.ball = BallWidget()
        # self.ball.build()
        # self.add_widget(self.ball)
        # kivy.clock.Clock.schedule_interval(self.update, 1/30)

    def update(self, dt):
        self.ball.update(dt)

    def float_x_to_pixels(self, x):
        return x * self.screen_size.x

    def float_y_to_pixels(self, y):
        return y * self.screen_size.y

    def float_to_pixels(self, x, y):
        return (self.float_x_to_pixels(x), self.float_y_to_pixels(y))



class TanksApp(App):
    pass

if __name__ == '__main__':
    TanksApp().run()