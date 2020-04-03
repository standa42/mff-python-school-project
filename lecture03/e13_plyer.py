#!/usr/bin/env python3

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from plyer import notification
from plyer import battery


class MyBox(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBox, self).__init__(orientation='vertical', **kwargs)

    def show_notification(self):
        notification.notify(title='Kivy Test App', message='Hello from Kivy', app_name='TestApp', ticker='Test')

    def show_battery(self):
        battery.get_state()
        lbl_text = 'Is charging: %s\nremaining: %f%%' % (battery.status["isCharging"], battery.status["percentage"])
        popup = Popup(title='Battery Info', content=Label(text=lbl_text), size_hint=(None, None), size=(200, 200))
        popup.open()


class KvEx13App(App):
    def build(self):
        return MyBox()


KvEx13App().run()

