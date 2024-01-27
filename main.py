from kivy.app import App

from interfaces import *

Window.borderless = True

class MainApp(App):
    def build(self):
        return Interface()


MainApp().run()
