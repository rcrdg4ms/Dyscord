from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.behaviors import HoverBehavior
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.properties import NumericProperty
from kivy.effects.scroll import ScrollEffect
from mouse import Cursor, Window
from database import localdb, db


class Groups_scroll(ScrollView):
    effect_cls = ScrollEffect

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        usergroups = db.get(localdb.get('user'))['groups']
        boxl = Boxlg()

        boxl.add_widget(Directmessages())
        boxl.height = (48+8)

        widget = Widget()
        widget.size_hint_y = None
        widget.height = 10
        boxl.add_widget(widget)
        boxl.height += 10

        for groupid in usergroups:
            boxl.add_widget(Group(groupid))
            boxl.height += 48+8

        self.add_widget(boxl)
        
    
    def on_touch_move(self, touch):
        ...

    def on_scroll_start(self, touch, check_children=True):
        return super().on_scroll_start(touch, check_children)


class Boxlg(BoxLayout):
    size_hint_y = None
    orientation = 'vertical'

    def change_group(self, groupid):
        if localdb.get()['last_group'] == groupid:
                return
        for children in self.children:
            if type(children) != Widget:
                if children.groupid == localdb.get()['last_group']:
                    Animation(
                        pingsize = 1,

                        duration = .1
                    ).start(children)

                elif children.groupid == groupid:
                    Animation(
                        pingsize = 42,

                        duration = .1
                    ).start(children)
        localdb.change('last_group', groupid)
        Window.children[0].reload_channels()

class Group_popup(ScrollView):
    def label_on(self, parent):
        self.size_hint_x = 1
        self.pos_y = parent.pos[1]
        self.groupname = parent.groupname

        Animation(
            alpha = 1,
            
            d = .1
        ).start(self)
    

    def label_off(self):
        self.size_hint_x = None
        self.width = 0

        Animation(
            alpha = 0,
            
            d = .1
        ).start(self)


    def on_scroll_start(self, touch, check_children=True):
        ...


class Group_button(Button, HoverBehavior):
    def on_enter(self):
        Window.children[0].ids.grouppopup.label_on(self.parent)

        Animation(
            radius = 45/4+45/8,
            color_on = self.parent.colors[1],
            
            d = .1
        ).start(self)

        Cursor.add('hand')

        self.parent.enter()
    
    def on_leave(self):
        Window.children[0].ids.grouppopup.label_off()

        Animation(
            radius = 45/2,
            color_on = self.parent.colors[0],

            d = .1
        ).start(self)

        Cursor.remove()

        self.parent.leave()

    
    def on_press(self):
        self.pos_y = self.pos[1]
        self.pos = (self.pos[0], self.pos[1]-1)
    
    def on_release(self):
        self.pos = (self.pos[0], self.pos_y)
        self.parent.parent.change_group(self.parent.groupid)


class Group(Widget):
    def __init__(self, groupid = None, **kwargs):
        super().__init__(**kwargs)

        self.groupid = groupid
        if self.groupid == localdb.get('last_group'):
            self.pingsize = 42

        if groupid:
            source = db.get(groupid)['source']
            if source:
                self.source = source

    @property
    def groupname(self):
        if self.groupid != None:
            return db.get(self.groupid)['name']
        return self._groupname

    def enter(self):
        Animation(
            pingsize = 20 if self.groupid != localdb.get()['last_group'] else self.pingsize,

            duration = .1
        ).start(self)
    
    def leave(self):
        Animation(
            pingsize = 1 if self.groupid != localdb.get()['last_group'] else self.pingsize,

            duration = .1
        ).start(self)


class Directmessages(Group):
    ...


class Groups(FloatLayout):
    ...