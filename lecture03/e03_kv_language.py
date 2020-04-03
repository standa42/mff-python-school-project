#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class KvEx03App(App):
    def build(self):
        return GridLayout()


if __name__ == "__main__":
    KvEx03App().run()
