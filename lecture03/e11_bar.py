#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.actionbar import ActionBar


class KvEx11App(App):
    def build(self):
        return ActionBar()


if __name__ == "__main__":
    KvEx11App().run()
