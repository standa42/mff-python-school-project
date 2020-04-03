#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout


class RootWidget(GridLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        for i in range(3):
            cb = CustomBtn()
            self.add_widget(cb)


class CustomBtn(Widget):

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print('Touched in the widget')
        else:
            print('Touched outside the widget')
        return super().on_touch_down(touch)


class TestApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    TestApp().run()
