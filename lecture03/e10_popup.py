#!/usr/bin/env python3


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout


class TestApp(App):
    def build(self):
        btn = Button(text='Hello World')
        btn.bind(on_press=self.on_button_press)
        return btn

    def on_button_press(self, button):
        # popup = Popup(title='My Popup', content=Label(text='Test'), size_hint=(None, None), size=(200, 200))
        # popup.open()
        layout = GridLayout(cols=1, padding=10)
        popup_label = Label(text="Pop-up")
        close_button = Button(text="Close")
        layout.add_widget(popup_label)
        layout.add_widget(close_button)
        popup = Popup(title='My Popup',  content=layout, size_hint=(None, None), size=(200, 200), auto_dismiss=False)
        popup.open()
        close_button.bind(on_press=popup.dismiss)


if __name__ == '__main__':
    TestApp().run()
