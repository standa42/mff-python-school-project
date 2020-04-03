
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

import numpy as np

# from kivy.config import Config
# Config.set('graphics', 'resizable', False)


# Ellipse:
#                 pos: 100, 100
#                 size: 200 * wm.value, 201 * hm.value
#                 source: 'data/logo/kivy-icon-512.png'
#                 angle_start: e1.value
#                 angle_end: e2.value
class TankWidget(Widget):
    def build(self):
        with self.canvas:
            Color(1, 0.2, 0)
            Rectangle(pos=(300, 300), size=(200, 200))



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

class MenuScreen(Screen):
    def _go_to_hall_of_fame(self):
        self.parent.get_screen("HallOfFameScreen").make_editable(False)
        self.parent.current = 'HallOfFameScreen'

class GameScreen(Screen):
    def on_pre_enter(self):
        game_widget = self.ids.game_widget
        game_widget.clear()
        # initGame

    def on_enter(self):
        game_widget = self.ids.game_widget
        with self.canvas.before:
            Color(0, 0, 0.7)
        game_widget.createMap()

        # tank = TankWidget()
        # tank.build()
        # self.add_widget(tank)

class HallOfFameScreen(Screen):
    def make_editable(self, editable = True):
        self.editable = editable
        scores_holder = self.ids.scores_holder
        scores_holder.clear_widgets()

        scores = []

        Path("./scores/").mkdir(parents=True, exist_ok=True)
        if os.path.isfile('./scores/scores.txt') and os.stat('./scores/scores.txt').st_size > 0:
            with open('./scores/scores.txt', 'r') as f:
                content = f.readlines()
                scores = [line.strip('\n') for line in content]

        scores = scores + ["-Not filled yet-"] * (5-len(scores))

        if(editable):
            scores_holder.add_widget(TextInput(hint_text='Write your name..', id='score_input'))
            scores = scores[:-1]
        
        for score in scores:
            scores_holder.add_widget(Label(text=score))

    def on_pre_leave(self):
        self.save_name()
    
    def save_name(self):
        if(self.editable):
            scores = []

            Path("./scores/").mkdir(parents=True, exist_ok=True)
            with open('./scores/scores.txt', 'r+') as f:
                content = f.readlines()
                scores = [line.strip('\n') for line in content]

            new_name = self.ids.scores_holder.children[-1].text
            if(not new_name.strip()):
                new_name = "Left empty"
            scores = [new_name] + scores 
            if(len(scores) > 5):
                scores = scores[:5]

            with open('./scores/scores.txt', 'w') as f:
                f.write("\n".join(scores))



class TanksApp(App):
    pass

if __name__ == '__main__':
    TanksApp().run()