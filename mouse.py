from kivy.core.window import Window
from pynput.mouse import Controller

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


Mouse = Controller()
Windowv = _Window()
Cursor = _Cursor()
