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

    def on_touch_down(self, touch):
        print(f'Position: {touch.pos}, Double tap: {touch.is_double_tap}, Triple tap: {touch.is_triple_tap}')
        if touch.is_double_tap:
            print(' - interval is', touch.double_tap_time)
            print(' - distance between previous is', touch.double_tap_distance)
        elif touch.is_triple_tap:
            print(' - interval is', touch.triple_tap_time)
            print(' - distance between previous is', touch.triple_tap_distance)
        return super().on_touch_down(touch)


class TestApp(App):

    def build(self):
        return RootWidget()


if __name__ == '__main__':
    TestApp().run()
