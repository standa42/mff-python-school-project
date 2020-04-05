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
from Game import GameScreen
from GameState import GameState
from Ball import BallWidget

from circular_progress_bar import CircularProgressBar

# Ban resizing
# from kivy.config import Config
# Config.set('graphics', 'resizable', False)

   

class TanksApp(App):
    pass

if __name__ == '__main__':
    TanksApp().run()