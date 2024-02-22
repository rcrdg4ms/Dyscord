from kivy.uix.floatlayout import FloatLayout
from interfaces.windowborder import Windowborder
from interfaces.groups import Group, Group_popup
from interfaces.channels import Channels


class Interface(FloatLayout):
    def reload_channels(self):
        self.ids.mainfloat.remove_widget(self.ids.mainfloat.children[1])
        channels = Channels()
        self.ids.mainfloat.add_widget(channels, 1)
