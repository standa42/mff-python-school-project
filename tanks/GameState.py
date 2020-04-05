         
import kivy
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from random import random, randint
from kivy.graphics import Color, Ellipse, Line, Rectangle
import kivy.clock
from kivy.core.window import Window
import kivy.core.text

import numpy as np
import math

from HallOfFame import HallOfFameScreen
from Menu import MenuScreen
from Map import MapWidget
from Point import Point
from Tank import TankWidget
from Ball import BallWidget

class GameState():
    def __init__(self, number_of_players):
        self.number_of_players = number_of_players
        self.alive_players = number_of_players
        self.tanks = []
        self.ball_flies = False
        self.current_tank = 0

    def is_ball_flying(self):
        return self.ball_flies

    def get_current_tank(self):
        return self.tanks[self.current_tank]

    def next_tank(self, hit_tank):
        to_remove = None
        if hit_tank is not None:
            curr_index = self.current_tank
            removed_index = list(map(lambda x: x.player_number, self.tanks)).index(hit_tank)
            self.current_tank -= 1
            to_remove = self.tanks[removed_index]
            del self.tanks[removed_index]
            if removed_index > self.current_tank:
                self.current_tank += 1
            self.alive_players -= 1
        self.current_tank += 1
        if self.current_tank >= self.alive_players:
            self.current_tank = 0
        return self.tanks[self.current_tank], to_remove

    def make_ball(self, power, angle):
        self.ball_flies = True
        self.tanks[self.current_tank].barrel_rotation = angle


        pos = self.rotate(
            (self.tanks[self.current_tank].position.x , self.tanks[self.current_tank].position.y ),
            (self.tanks[self.current_tank].position.x, self.tanks[self.current_tank].position.y + TankWidget.tank_size//2 + TankWidget.tank_barrel_size.y + 5),
            math.radians(angle)
        )

        ball = BallWidget()
        ball.build(position = Point(pos[0], pos[1]), velocity = Point(pos[0] - self.tanks[self.current_tank].position.x, pos[1] - self.tanks[self.current_tank].position.y))
        return ball

    

    def rotate(self, origin, point, angle):
        """
        https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
        Rotate a point counterclockwise by a given angle around a given origin.
        The angle should be given in radians.
        """
        ox, oy = origin
        px, py = point

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy
