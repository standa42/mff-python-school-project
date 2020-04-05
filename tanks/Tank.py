import kivy
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.graphics import Rotate
from kivy.graphics.context_instructions import PopMatrix, PushMatrix

from Point import Point

class TankWidget(Widget):
    tank_size = 28
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