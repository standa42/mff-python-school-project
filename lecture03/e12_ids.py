#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty


class MyWidget(GridLayout):
    password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_submit(self):
        print(f'username: {self.ids.username.text}, Password: {self.password.text}')

    def on_reset(self):
        self.ids.username.text = ''
        self.password.text = ''


class KvEx12App(App):
    def build(self):
        return MyWidget()


if __name__ == "__main__":
    KvEx12App().run()
