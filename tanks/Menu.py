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

from circular_progress_bar import CircularProgressBar

class MenuScreen(Screen):
    def _go_to_hall_of_fame(self):
        self.parent.get_screen("HallOfFameScreen").make_editable(False)
        self.parent.current = 'HallOfFameScreen'

    def _go_to_game(self):
        self.parent.get_screen("GameScreen").set_scene(number_of_players = int(self.ids.number_of_players.text), screen_size = self.size)
        self.parent.current = 'GameScreen'