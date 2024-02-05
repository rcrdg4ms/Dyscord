from kivy.app import App
from kivy.core.window import Window

from interfaces import *

Window.borderless = True

class MainApp(App):
    def build(self):
        return Interface()


MainApp().run()
