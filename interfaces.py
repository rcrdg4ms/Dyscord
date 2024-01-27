from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from pynput.mouse import Controller
from kivymd.uix.behaviors import HoverBehavior
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.properties import NumericProperty


Mouse = Controller()

class _Cursor:
    __cursor__ = []

    def add(self, cursor):
        self.__cursor__.append(cursor)
        Window.set_system_cursor(self.__cursor__[-1])

    
    def remove(self):
        if self.size > 0:
            self.__cursor__.pop(0)

        if self.size == 0:
            Window.set_system_cursor('arrow')

    @property
    def size(self):
        return len(self.__cursor__)

class _Window:
    fullscreen = False
    left = 0
    top = 0
    size = (0, 0)
    Window.maximize()
    Maxsize = (Window.size[0], Window.size[1]+22)
    Window.restore()

Cursor = _Cursor()
Windowv = _Window()

class Interface(FloatLayout):
    ...

class Windowborder(FloatLayout):
    ...

class Windowborder_move(Button):
    __press__ = False
    lastpos = (0, 0)

    def on_press(self):
        self.__press__ = True
        self.parent.resizepress = True
        self.initpos = Mouse.position
        self.lastpos = self.initpos
        self.initwindowpos = (Window.left, Window.top)
        self.initwindowsize = Window.size

    def on_touch_move(self, touch):
        if self.__press__:
            mouseposition = Mouse.position
            if Windowv.fullscreen:
                Windowv.fullscreen = False
                Window.size = Windowv.size

                self.initwindowpos = (
                    round(mouseposition[0] - ((touch.pos[0]*Windowv.size[0])/Windowv.Maxsize[0]))-5,
                    self.initwindowpos[1]
                )

                self.parent.windowglobalheight = 5

            if mouseposition != self.lastpos:
                self.lastpos = mouseposition
                Window.left = self.initwindowpos[0] + mouseposition[0] - self.initpos[0]
                Window.top = self.initwindowpos[1] + mouseposition[1] - self.initpos[1]
    
    def on_release(self):
        self.__press__ = False
        self.parent.resizepress = False


class Windowborder_resize(Windowborder_move, HoverBehavior):
    def on_enter(self):
        if not self.parent.resizepress:
            Cursor.add(self.cursor_to_set)

    def on_leave(self):
        if not self.parent.resizepress:
            Cursor.remove()


    def on_touch_move(self, touch):
        if self.__press__:
            mouseposition = Mouse.position
            if mouseposition != self.lastpos:
                self.lastpos = mouseposition
                mousedeslocation = (mouseposition[0] - self.initpos[0], mouseposition[1] - self.initpos[1])

                if self.name == 'bottom_left':
                    Window.left = self.initwindowpos[0] + mousedeslocation[0]
                    Window.size = (self.initwindowsize[0] - mousedeslocation[0], self.initwindowsize[1] + mousedeslocation[1])
                
                elif self.name == 'bottom':
                    Window.size = (Window.size[0], self.initwindowsize[1] + mousedeslocation[1])
                
                elif self.name == 'bottom_right':
                    Window.size = (self.initwindowsize[0] + mousedeslocation[0], self.initwindowsize[1] + mousedeslocation[1])
                
                elif self.name == 'top_left':
                    Window.left = self.initwindowpos[0] + mousedeslocation[0]
                    Window.top = self.initwindowpos[1] + mousedeslocation[1]
                    Window.size = (self.initwindowsize[0] - mousedeslocation[0], self.initwindowsize[1] - mousedeslocation[1])
                
                elif self.name == 'top':
                    Window.top = self.initwindowpos[1] + mousedeslocation[1]
                    Window.size = (Window.size[0], self.initwindowsize[1] - mousedeslocation[1])
                
                elif self.name == 'top_right':
                    Window.top = self.initwindowpos[1] + mousedeslocation[1]
                    Window.size = (self.initwindowsize[0] + mousedeslocation[0], self.initwindowsize[1] - mousedeslocation[1])
                
                elif self.name == 'left':
                    Window.left = self.initwindowpos[0] + mousedeslocation[0]
                    Window.size = (self.initwindowsize[0] - mousedeslocation[0], Window.size[1])

                elif self.name == 'right':
                    Window.size = (self.initwindowsize[0] + mousedeslocation[0], Window.size[1])


class Windowborder_buttons(Button):
    alpha = NumericProperty(0)
    def enter(self, cursor=True):
        self.alpha = self.intensity
        Cursor.add('hand')

    def leave(self, cursor=True):
        self.alpha = 0
        Cursor.remove()

    def on_press(self):
        if self.text == '-':
            Window.minimize()
        elif self.text == '◻':
            if not Windowv.fullscreen:
                Windowv.left = Window.left
                Windowv.top = Window.top
                Windowv.size = Window.size
                Window.left = 0
                Window.top = 0
                Window.size = Windowv.Maxsize
                self.parent.parent.windowglobalheight = -1

            else:
                Window.left = Windowv.left
                Window.top = Windowv.top
                Window.size = Windowv.size
                self.parent.parent.windowglobalheight = 5
            Windowv.fullscreen = not Windowv.fullscreen
        else:
            Window.close()
