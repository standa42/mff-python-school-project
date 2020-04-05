import kivy
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from Tank import TankWidget
from Point import Point
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics import Mesh
from pathlib import Path
import os

class HallOfFameScreen(Screen):
    def make_editable(self, editable = True, player_won_color = None, size_hint = None):
        self.editable = editable
        scores_holder = self.ids.scores_holder
        scores_holder.clear_widgets()

        if player_won_color != None:
            with self.canvas:
                # green terrain
                Color(player_won_color.r, player_won_color.g, player_won_color.b)
                self.mesh = Mesh(vertices=[0,0,0,0 ,0,size_hint.y,0,0 ,size_hint.x,size_hint.y,0,0 , size_hint.x,0,0,0], indices=[0,1,2,3], mode='triangle_fan')

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