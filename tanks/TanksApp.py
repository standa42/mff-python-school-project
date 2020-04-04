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
from Tank import TankWidget

import numpy as np

import kivy.clock

from kivy.graphics import Rotate
from kivy.graphics.context_instructions import PopMatrix, PushMatrix
from kivy.core.window import Window

import kivy.core.text

from circular_progress_bar import CircularProgressBar

import scipy.ndimage

import math

# Bans resize
# from kivy.config import Config
# Config.set('graphics', 'resizable', False)

class BallWidget(Widget):
    ball_size = 7

    def build(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0,0,0)
            Ellipse(pos=(self.position.x - BallWidget.ball_size//2, self.position.y - BallWidget.ball_size//2), size=(BallWidget.ball_size, BallWidget.ball_size), segments = 30)

    def update_position(self, dt, power, screen_size):
        self.position.x += self.velocity.x * 0.4 * (2.0 *power/100) * dt * 40 
        self.position.y += self.velocity.y * 0.4 * (2.0 *power/100) * dt * 40
        self.velocity.y -= 1.0
        self._check_edges(screen_size)
        self.draw()

        if self.position.y < 0:
            return False
        else:
            return True
        pass           

    def _check_edges(self, screen_size):
        if self.position.x < 0 or self.position.x > screen_size.x:
            self.velocity.x *= -1





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

    def next_tank(self):
        self.current_tank = (self.current_tank + 1) % self.alive_players
        return self.tanks[self.current_tank]

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

class GameScreen(Screen):
    colors = [
        Color(0.933, 0.090, 0.117), # Red
        Color(0.090, 0.368, 0.933), # Blue
        Color(0.933, 0.090, 0.878), # Purple
        Color(0.941, 0.627, 0.141), # Orange
        Color(0.3, 0.5, 0.2), # Dark green
        Color(0, 0, 0 )  # Black
    ]

    #region Widget lifecycle events
    def set_scene(self, number_of_players, screen_size):
        self.screen_size = Point(screen_size[0], screen_size[1])
        self.game_state = GameState(number_of_players)

    def on_pre_enter(self):
        # map
        map_widget = self.ids.map_widget
        map_widget.clear()
        map_widget.generate_terrain()

        # tanks
        tanks_positions = map_widget.generate_tanks_positions(self.game_state.number_of_players)
        self.game_state.tanks = []
        for i in range(self.game_state.number_of_players):
            tank = TankWidget()
            tank.build(i, GameScreen.colors[i], tanks_positions[i])
            self.add_widget(tank)
            self.game_state.tanks.append(tank)

        # progress bar
        self.progress_bar = CircularProgressBar()
        self.progress_bar.thickness = 6
        self.progress_bar.value = 0
        self.progress_bar.widget_size = int(self.screen_size.y * 0.18)
        self.progress_bar.label.text = ""
        self.progress_bar.label = kivy.core.text.Label(text="{}%", font_size=int(self.screen_size.y * 0.05))
        self.progress_bar.pos = [self.screen_size.x//2 - self.progress_bar.widget_size // 2, 15]
        self.progress_bar.progress_colour = [GameScreen.colors[0].r, GameScreen.colors[0].g, GameScreen.colors[0].b]
        #self.progress_bar.background_colour = [0.639, 0.639, 0.639]
        self.add_widget(self.progress_bar)
        self.progress_bar._refresh_text()
        self.progress_bar._draw()
        

    def on_leave(self):
        for tank in self.game_state.tanks:
            self.remove_widget(tank)
        self.ids.map_widget.clear()
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        kivy.clock.Clock.unschedule(self.update)
        self.remove_widget(self.progress_bar)
        if 'ball' in locals() and self.ball is not None:
            self.remove_widget(self.ball)

    def on_enter(self):
        kivy.clock.Clock.schedule_interval(self.update, 1/40)

        # keyboard
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.space_pressed = False
        self.space_unpressed = False
        self.left_pressed = False
        self.right_pressed = False

        # vars
        self.angle = 0
        self.power = 0

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    #endregion

    #region Game Logic
    def update(self, dt):
        tank = self.game_state.get_current_tank()

        if self.game_state.is_ball_flying():
            # ball fyzics
            valid_pos = self.ball.update_position(dt, self.power, self.screen_size)
            
            
            
            
            
            
            if not valid_pos:
                self.remove_widget(self.ball)
                self.game_state.ball_flies = False
                next_tank = self.game_state.next_tank()
                self.angle = next_tank.barrel_rotation
                self.power = 0
                self.progress_bar.value = 0
                self.progress_bar.progress_colour = [next_tank.color.r, next_tank.color.g, next_tank.color.b]
                self.progress_bar._draw()
            # TODO: ball hits st - solve it, check game end, end turn
            pass
        else:
            # left,right => angle
            if self.left_pressed != self.right_pressed:
                self.angle = np.clip(self.angle + (1.0 * ((-1) if self.right_pressed else 1)), -90, 90)
                tank.update(self.angle)
            # space => power
            if self.space_pressed:
                self.power += 0.5
                self.progress_bar.value = int(np.clip(self.power, 0, 100))
            # space unpress || full power => make ball
            if self.space_unpressed or self.power == 100:
                self.space_pressed = False
                self.space_unpressed = False
                self.ball = self.game_state.make_ball(self.power, self.angle)
                self.add_widget(self.ball)


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        _, key = keycode
        if not self.game_state.is_ball_flying():
            if key == 'left':
                self.left_pressed = True
            elif key == 'right':
                self.right_pressed = True
            elif key == 'spacebar':
                self.space_pressed = True

    def _on_keyboard_up(self, keyboard, keycode):
        _, key = keycode
        if key == 'left':
            self.left_pressed = False
        elif key == 'right':
            self.right_pressed = False
        elif key == 'spacebar':
            self.space_pressed = False
            self.space_unpressed = True
    #endregion

    #region Helper functions
    def float_x_to_pixels(self, x):
        return x * self.screen_size.x

    def float_y_to_pixels(self, y):
        return y * self.screen_size.y

    def float_to_pixels(self, x, y):
        return (self.float_x_to_pixels(x), self.float_y_to_pixels(y))
    #endregion


class TanksApp(App):
    pass

if __name__ == '__main__':
    TanksApp().run()