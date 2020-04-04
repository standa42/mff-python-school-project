
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

class GameScreen(Screen):
    def set_scene(self, number_of_players, screen_size):
        self.number_of_players = number_of_players
        self.screen_size = Point(screen_size[0], screen_size[1])

    def on_pre_enter(self):
        map_widget = self.ids.map_widget
        map_widget.clear()
        map_widget.generate_terrain()
        map_widget.generate_tanks_positions(self.number_of_players)

        tank = TankWidget()
        tank.build()
        self.add_widget(tank)


    def on_leave(self):
        self.ids.map_widget.clear()

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