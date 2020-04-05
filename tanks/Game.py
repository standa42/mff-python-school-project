
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
from GameState import GameState

from circular_progress_bar import CircularProgressBar

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
        self.map_widget = self.ids.map_widget
        self.map_widget.clear()
        self.map_widget.generate_terrain()

        # tanks
        tanks_positions = self.map_widget.generate_tanks_positions(self.game_state.number_of_players)
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
        self.progress_bar.pos = [self.screen_size.x//2 - self.progress_bar.widget_size // 2, 17]
        self.progress_bar.progress_colour = [GameScreen.colors[0].r, GameScreen.colors[0].g, GameScreen.colors[0].b, 0.8]
        self.progress_bar.background_colour = [0.26,0.26,0.26,0.4]
        #self.progress_bar.background_colour = [0.639, 0.639, 0.639]
        self.add_widget(self.progress_bar)
        self.progress_bar._refresh_text()
        self.progress_bar._draw()

        # controls prompt
        self.prompt_label = Label(text = 'left/right arrow => angle, space => power', size_hint= (0.5, 0.03), pos_hint= {"center_x":0.5, "center_y":0.5})
        self.add_widget(self.prompt_label)

    def on_leave(self):
        for tank in self.game_state.tanks:
            self.remove_widget(tank)
        self.ids.map_widget.clear()
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        kivy.clock.Clock.unschedule(self.update)
        self.remove_widget(self.progress_bar)
        if hasattr(self,'ball') and self.ball is not None:
            self.remove_widget(self.ball)
        if hasattr(self,'prompt_label') and self.prompt_label is not None:
            self.remove_widget(self.prompt_label)

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
            valid_pos = True 
            self.ball.update_position(dt, self.power, self.screen_size)

            # TODO: solve ball hit into another tanks
            hit_tank = None
            for checked_tank in self.game_state.tanks:
                if checked_tank.player_number != tank.player_number:
                    if np.sqrt((checked_tank.position.x - self.ball.position.x)**2 + (checked_tank.position.y - self.ball.position.y)**2) < (TankWidget.tank_size//2) + 4.5:
                        hit_tank = checked_tank.player_number
                        valid_pos = False

            if valid_pos:
                hit_terrain = self.map_widget.collides_with_ball(self.ball.position, self.game_state.tanks)


            
            
            
            
            if not valid_pos or hit_terrain:
                self.remove_widget(self.ball)
                self.game_state.ball_flies = False
                next_tank, removed_tank = self.game_state.next_tank(hit_tank)
                if removed_tank is not None:
                    self.remove_widget(removed_tank)
                self.angle = next_tank.barrel_rotation
                self.power = 0
                self.progress_bar.value = 0
                self.progress_bar.progress_colour = [next_tank.color.r, next_tank.color.g, next_tank.color.b, 0.8]
                self.progress_bar._draw()
                self.space_pressed = False
                self.space_unpressed = False
                
            if len(self.game_state.tanks) == 1:
                self.parent.get_screen("HallOfFameScreen").make_editable(True, self.game_state.tanks[0].color, size_hint = Point(self.size[0], self.size[1] // 20))
                self.parent.current = 'HallOfFameScreen'

            pass
        else:
            # left,right => angle
            if self.left_pressed != self.right_pressed:
                self.angle = np.clip(self.angle + (1.0 * ((-1) if self.right_pressed else 1)), -90, 90)
                tank.update(self.angle)
            # space => power
            if self.space_pressed:
                self.power += 0.4
                self.progress_bar.value = int(np.clip(self.power, 0, 100))
            # space unpress || full power => make ball
            if self.space_unpressed or self.power == 100:
                self.space_pressed = False
                self.space_unpressed = False
                self.ball = self.game_state.make_ball(self.power, self.angle)
                self.add_widget(self.ball)


    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        _, key = keycode

        if self.prompt_label is not None:
            self.remove_widget(self.prompt_label)
            self.prompt_label = None

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
            if self.space_pressed:
                self.space_unpressed = True
            self.space_pressed = False
            
    #endregion

    #region Helper functions
    def float_x_to_pixels(self, x):
        return x * self.screen_size.x

    def float_y_to_pixels(self, y):
        return y * self.screen_size.y

    def float_to_pixels(self, x, y):
        return (self.float_x_to_pixels(x), self.float_y_to_pixels(y))
    #endregion
