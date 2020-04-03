#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout


class RootWidget(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cb = CustomBtn()
        self.add_widget(cb)


class CustomBtn(Widget):

    def on_touch_move(self, touch):
        print(touch.profile)
        return super().on_touch_move(touch)


class TestApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    TestApp().run()
