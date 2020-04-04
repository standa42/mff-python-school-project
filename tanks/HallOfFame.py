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