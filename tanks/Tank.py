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

class TankWidget(Widget):
    tank_size = 26
    tank_barrel_size = Point(5,7)

    def build(self, player_number, color, position):
        self.player_number = player_number
        self.color = color
        self.position = position

        self.barrel_rotation = 0

        self.draw()
        

    def draw(self):
        self.canvas.clear()
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
    
    def update(self, barrel_rotation):
        self.barrel_rotation = barrel_rotation
        self.draw()