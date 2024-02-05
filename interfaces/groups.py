from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.behaviors import HoverBehavior
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.effects.scroll import ScrollEffect
from mouse import Cursor
import json


class Groups_scroll(ScrollView):
    effect_cls = ScrollEffect

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        usergroups = db.get()[localdb.get()['user']]['groups']
        floatl = Floatl()

        floatl.size_hint_y = None
        floatl.height = (48+8)*(len(usergroups)+1)+10
        
        direct = Directmessages(len(usergroups))
        direct.position_y = direct.position_y+10
        floatl.add_widget(direct)

        num = len(usergroups)-1
        for groupid in usergroups:
            floatl.add_widget(Group(num, groupid))
            num -= 1 

        self.add_widget(floatl)

    def on_scroll_start(self, touch, check_children=True):
        if self.parent.inscrollarea:
            return super().on_scroll_start(touch, check_children)
        
    
    def on_touch_move(self, touch):
        ...


class Floatl(FloatLayout):
    ...


class _localdb:
    def get(self):
        return json.load(open('local.json', 'r'))

    def change(self, key, value):
        db = self.get()
        db[key] = value
        json.dump(db, open('local.json', 'w'), indent=4)

class _db:
    def get(self):
        return json.load(open('Database.json', 'r'))
    
db = _db()
localdb = _localdb()


class Group_button(Button, HoverBehavior):
    def on_enter(self):
        Animation(
            radius = 45/4+45/8,
            color_on = self.parent.colors[1],
            
            d = .1
        ).start(self)
        Cursor.add('hand')

        self.parent.enter()
    
    def on_leave(self):
        Animation(
            radius = 45/2,
            color_on = self.parent.colors[0],

            d = .1
        ).start(self)
        Cursor.remove()

        self.parent.leave()

    
    def on_press(self):
        self.pos = (self.pos[0], self.parent.position_y-1)
    
    def on_release(self):
        self.pos = (self.pos[0], self.parent.position_y)
        localdb.change('group', self.parent.groupid)


class Group(FloatLayout):
    def __init__(self, num, groupid = None, **kwargs):
        super().__init__(**kwargs)
        self.position_y = ((48+8)*num)+4

        self.groupid = groupid

        if groupid:
            source = db.get()[groupid]['source']
            if source:
                self.source = source

    def enter(self):
        if self.groupid:
            self.groupname = db.get()[self.groupid]['name']
        Animation(
            alpha = 1,
            pingsize = 20,

            duration = .1
        ).start(self)
    
    def leave(self):
                Animation(
            alpha = 0,
            pingsize = 1,

            duration = .1
        ).start(self)


class Directmessages(Group):
    ...


class Groups(FloatLayout):
    ...