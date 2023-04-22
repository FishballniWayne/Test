import os, sys
import sqlite3
import datetime
from kivy.config import Config
Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '700')
from kivymd.app import MDApp
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.storage.jsonstore import JsonStore
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.snackbar import BaseSnackbar
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

from kivy.resources import resource_add_path, resource_find

#Builder.load_file('test.kv')
#Define our different screens

class CustomSnackbar(BaseSnackbar):
    text = StringProperty(None)
    icon = StringProperty(None)
    font_size = NumericProperty("15sp")
    
class MainLayout(FloatLayout):

    def __init__(self, *args, **kwargs):  
        super().__init__(*args, **kwargs)
        self.store = JsonStore("loggedUser.json")
        
        try:
            if self.store.get('UserInfo') ['firstname'] != "":
                self.screen_manager.current = 'dashboard_screen'
        except KeyError:
                self.screen_manager.current = 'login_screen'


    
    def open_custom_snackbar(self):
        snackbar = Snackbar(
            text="[color=#ffffff]Yo! this is a custom snackbar![/color]",
            font_size ="16dp",
            bg_color = "orange",
            snackbar_x = "10dp",
            snackbar_y = "10dp",
            size_hint_x = (Window.width - (dp(10) * 2)) / Window.width,
        )
        snackbar.open()

    def open_icon_snackbar(self):
        snackbar = CustomSnackbar(
            text = "This is a sample snackbar error!",
            icon = "close-circle",
            snackbar_x = "10dp",
            snackbar_y = "10dp",
            size_hint_x = (Window.width - (dp(10) * 2)) / Window.width,
            bg_color = "#B71C1C"
        )
        snackbar.open()    
                
    def slide(self,screens,arrow):
        self.ids.screen_manager1.current = screens
        self.ids.screen_manager1.transition.direction = arrow
    
    def login(self):
        inp_username = self.ids.log_username.text
        inp_password = self.ids.log_password.text
        dbconn = sqlite3.connect('kivysql.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = dbconn.cursor()
        dbcursor.execute("SELECT * FROM mstuser WHERE mstuser.username = :var_username AND mstuser.password = :var_password",
                         {
                             'var_username': inp_username,
                             'var_password': inp_password
                         })
        records = dbcursor.fetchall()
        
        if not records:
            print("No record created")
        else:
            for user in records:
                print(f"Username: {user[1]}\nFirstName: {user[2]}\nLastName: {user[3]}")
                self.store.put('UserInfo',code=user[0],firstname=user[2],lastname=user[3],username=user[1])
            print("Record Exist")
            dbconn.commit()
            dbconn.close()
            self.ids.screen_manager1.current = "dashboard_screen"
            self.ids.screen_manager1.transition.direction = "left"
        
    def register(self):
        inp_username = self.ids.username.text
        inp_firstname = self.ids.firstname.text
        inp_lastname = self.ids.lastname.text
        inp_email = self.ids.email.text
        inp_password = self.ids.password.text
        
        dbconn = sqlite3.connect('kivysql.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        dbcursor = dbconn.cursor()
        #dbcursor.execute("SELECT * FROM mstuser")
        dbcursor.execute("INSERT INTO mstuser (username, first_name, last_name, email, password, created_at, updated_at) VALUES (:var_username, :var_firstname, :var_lastname, :var_email, :var_password, :var_created_at, :var_updated_at)",
                         {
                             'var_username' : inp_username,
                             'var_firstname' : inp_firstname,
                             'var_lastname' : inp_lastname,
                             'var_email' : inp_email,
                             'var_password' : inp_password,
                             'var_created_at': datetime.datetime.now(),
                             'var_updated_at': datetime.datetime.now(),
                         })
        dbconn.commit()
        dbconn.close()
        self.ids.screen_manager1.current = "login_screen"
        self.ids.screen_manager1.transition.direction = "right"        
        pass
        
        
# Designate Our .kv design file 



class screenManagerApp(MDApp):
    DEBUG = True
    
    KV_FILES = {
        os.path.join('.', 'login.kv')
    }
    
    CLASSES = {
        "MainLayout": "screenManager"
    }
    
    def build(self):
            self.theme_cls.material_style = "M3"    
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette= "Blue"
            self.theme_cls.accent_palette= "Teal"
            return MainLayout()  
      
      
if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    screenManagerApp().run()
