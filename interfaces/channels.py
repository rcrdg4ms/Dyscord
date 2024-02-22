from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivymd.uix.behaviors import HoverBehavior
from kivy.properties import StringProperty, ColorProperty, NumericProperty
from kivy.effects.scroll import ScrollEffect
from database import localdb, db
from mouse import Cursor


Focus = False

class Channels_scroll(ScrollView):
    effect_cls = ScrollEffect

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        boxl = Channels_boxl()
        boxl.orientation = 'vertical'
        boxl.size_hint = (None, None)
        boxl.pos = self.pos
        boxl.width = 240
        boxl.height = 0

        groupid = localdb.get('last_group')

        for childrenid in db.get(groupid)['childrens']:
            childrentype = db.get(childrenid)['type']
            if childrentype == 'Category':
                children = Channels_category(childrenid)
            elif childrentype == 'Chat':
                children = Channels_chat(childrenid)
            
            boxl.height += children.height
            boxl.add_widget(children)

        self.add_widget(boxl)


class Channels_boxl(BoxLayout, HoverBehavior):
    def on_enter(self):
        self.parent.bar_inactive_color = (26/255, 27/255, 30/255, 1)
    
    def on_leave(self):
        self.parent.bar_inactive_color = (0,0,0, 0)


    def change_channel(self, chatid):
        last_chat = localdb.get('groups')[str(localdb.get('last_group'))]['last_chat']
        if last_chat == chatid:
            return
        
        for children in self.children:
            if type(children) == Channels_chat:
                if children.chatid == last_chat:
                    Animation(
                        alpha = 0,

                        d=.1
                    ).start(children.children[0])
                
                elif children.chatid == chatid:
                    Animation(
                        alpha = .25,

                        d=.1
                    ).start(children.children[0])

            else:
                for children in children.ids.chats.children:
                    if children.chatid == last_chat:
                        Animation(
                            alpha = 0,
                            label_color = (148/255, 155/255, 153/255, 1),

                            d=.1
                        ).start(children.children[0])
                
                    elif children.chatid == chatid:
                        Animation(
                            alpha = .25,
                            label_color = (1,1,1, 1),

                            d=.1
                        ).start(children.children[0])

        groups = localdb.get('groups')
        groups[str(localdb.get('last_group'))]['last_chat'] = chatid
        localdb.change('groups', groups)

class Channels_chat_button(Button, HoverBehavior):
    def on_enter(self):
        if not Focus:
            Cursor.add('hand')
            if localdb.get('groups')[str(localdb.get('last_group'))]['last_chat'] != self.parent.chatid:
                self.alpha = .1

    def on_leave(self):
        if not Focus:
            Cursor.remove()
            if localdb.get('groups')[str(localdb.get('last_group'))]['last_chat'] != self.parent.chatid:
                self.alpha = 0

    
    def on_release(self):
        parent = self.parent.parent
        
        if type(parent) == BoxLayout:
            parent = parent.parent.parent
            
        parent.change_channel(self.parent.chatid)

class Channels_category_button(Button, HoverBehavior):
    colors = [(148/255, 155/255, 164/255, 1), (1,1,1,1)]
    color_on = ColorProperty(colors[0])
    def on_release(self):
        self.parent.release(self.show)
        self.show = not self.show

    def on_enter(self):
        if not Focus:
            Cursor.add('hand')
            self.color_on = self.colors[1]

    def on_leave(self):
        if not Focus:
            Cursor.remove()
            self.color_on = self.colors[0]

class Channels_category(FloatLayout):
    category_name = StringProperty('')
    def __init__(self, categoryid, **kwargs):
        super().__init__(**kwargs)

        self.categoryid = categoryid
        self.category_name = db.get(categoryid)['name'].upper()
        self.on = False

        for chatid in db.get(categoryid)['chats']:
            chat = Channels_chat(chatid)
            self.ids.chats.height += chat.height
            self.ids.chats.add_widget(chat)


    def release(self, show):
        if show:
            self.save_childrens = self.ids.chats.children[:]
            self.ids.chats.clear_widgets()
            self.ids.chats.height -= self.save_childrens[0].height*len(self.save_childrens)
            self.parent.height -= self.save_childrens[0].height*len(self.save_childrens)
            
        else:
            for chatid in db.get(self.categoryid)['chats']:
                chat = Channels_chat(chatid)
                self.ids.chats.height += chat.height
                self.parent.height += chat.height
                self.ids.chats.add_widget(chat)
                

class Channels_chat(FloatLayout):
    chat_name = StringProperty('')
    def __init__(self, chatid, **kwargs):
        super().__init__(**kwargs)

        self.chatid = chatid
        chat_name = db.get(chatid)['name'].lower()
        chat_name = chat_name.replace(' ', '-')
        self.chat_name = chat_name


class Channels_group_label(Button, HoverBehavior):
    def on_enter(self):
        self.alpha = .2
        Cursor.add('hand')
    
    def on_leave(self):
        self.alpha = 0
        Cursor.remove()

    
    def on_release(self):
        self.show = not self.show
        self.parent.group_release(self.show)


class Channels_group_button(Button, HoverBehavior):
    color_back = ColorProperty((71/255, 82/255, 196/255, 1))
    def __init__(self, color_back, **kwargs):
        super().__init__(**kwargs)
        self.color_back = color_back

    def on_enter(self):
        self.alpha = 1
        Cursor.add('hand')
    
    def on_leave(self):
        self.alpha = 0
        Cursor.remove()

class Channels_group_popup(BoxLayout):
    def __init__(self, position_x, root_height, **kwargs):
        super().__init__(**kwargs)
        self.position_x = position_x
        self.root_height = root_height


    def start(self):
        Animation(
            size = (220, (7*34)+16),

            d = .1
        ).start(self)

        for num, x in enumerate([
            (1, 0, 0, 1),
            (1, .25, 0, 1),
            (1, 1, 0, 1),
            (0, 1, 0, 1),
            (0, 1, .75, 1),
            (0, 0, 1, 1),
            (.75, 0, .75, 1)
        ]):
            btn = Channels_group_button(color_back = x, text=f'button-{num}')

            Animation(
                size = (204, 32),
                color = (1,1,1,1),

                d = .1
            ).start(btn)
            
            self.add_widget(btn)


class Channels(FloatLayout):
    groupname = StringProperty('')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.groupid = localdb.get('last_group')
        self.groupname = db.get(self.groupid)['name']

    
    def group_release(self, show):
        global Focus
        if show:
            Focus = True
            w = Channels_group_popup(self.position_x, self.height)
            self.add_widget(w)
            w.start()
            return

        Focus = False
        self.remove_widget(self.children[0])
