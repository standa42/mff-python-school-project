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

import math

from HallOfFame import HallOfFameScreen
from Menu import MenuScreen
from Map import MapWidget
from Point import Point
from Tank import TankWidget

from circular_progress_bar import CircularProgressBar

class BallWidget(Widget):
    ball_size = 7

    def build(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.power = None
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0,0,0)
            Ellipse(
                pos=(self.position.x - BallWidget.ball_size//2, self.position.y - BallWidget.ball_size//2), 
                size=(BallWidget.ball_size, BallWidget.ball_size), 
                segments = 30
            )

    def update_position(self, dt, power, screen_size):
        # set initial velocity
        if self.power is None:
            self.power = power
            self.velocity.x *= 2.2 * self.power / 100
            self.velocity.y *= 2.2 * self.power / 100

        # update position
        self.position.x += self.velocity.x * 0.4 * dt * 40
        self.position.y += self.velocity.y * 0.4 * dt * 40

        # gravitational effect on velocity
        self.velocity.y -= 1.0
        self._check_edges(screen_size)
        self.draw()

    def _check_edges(self, screen_size):
        '''Rubber edges - reflect ball back into the scene'''
        if self.position.x < 0 or self.position.x > screen_size.x:
            self.velocity.x *= -1