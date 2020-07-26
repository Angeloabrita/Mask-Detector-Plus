import maskv
import dataControler
import cv2
import webbrowser
import kivy
import time
import os
import getpass
import cv2
import numpy as np
from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder
from kivy.clock import Clock
from camera import CameraCv
from kivy.core.image import Image as CoreImage
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
Config.set('graphics', 'resizable', True)
###---------------Screens classes--------------------######
#--  Main widget Screen
class Main(Screen):

    def on_enter(self):
        #set looop
        Clock.schedule_interval(self.update_date, .2)

    def on_leave(self):
        #stop loop
        Clock.unschedule(self.update_date)
    
    # update labels
    def update_date(self,dt):
        t = time.strftime(" %d/%m/%Y , %H:%M:%S")
        self.ids.lgAndDate.text = 'Hello '+ getpass.getuser()+ ' now is '+ t
        self.ids.now.text = ('Total people detected now %d' % maskv.nowTotal)
        self.ids.noMask.text = ('Toltal people\n without mask\n %d' % maskv.totalNoMask)
        self.ids.withMask.text = ('Toltal people\n with mask\n %d' % maskv.totalWithMask)
        self.ids.nowNoMask.text = ('People\n without mask\n now %d' % maskv.nowlNoMask)
        self.ids.nowWithMask.text = ('People\n with mask\n now %d' % maskv.nowlWithMask)
    
    def openURL(self,url):
        webbrowser.open(url)

    def open_mask_infraction_folder(self):
        try:
            os.startfile(maskv.os_path())
        except OSError:
            Popup("Erro!!", 'Erro to open folder')
              

    def plot_data(self):
        dataControler.plot_data()
    
    def export2Exel(self):
        dataControler.export_data()
        #--validation popup
        layout = GridLayout(cols = 1, padding = 10) 
        popupLabel = Label(text = "Sucess to save xmls at Documents folder as mask-detector.xmls") 
        closeButton = Button(text = "Ok")
        #okButton = Button(text = "Ok1")  
        layout.add_widget(popupLabel) 
        layout.add_widget(closeButton)
        
        # Instantiate the modal popup and display 
        popup = Popup(title = 'Sucess', 
                    content = layout, 
                    size_hint =(None, None), size =(600, 300))   
        popup.open()    
        # Attach close button press with popup.dismiss action 
        closeButton.bind(on_press = popup.dismiss)
      
    
#--config widget Screen
class Config(Screen):

    def removed(self, instance):
       
        dataControler.erase_data()
        
    
    def del_data(self):
        dataControler.export_data()
        #--validation popup
        layout = GridLayout(cols = 1, padding = 10) 
        popupLabel = Label(text = "Click delete if you are sure you want to delete all data. This action cannot be undone.") 
        closeButton = Button(text = "Get out!")
        okButton = Button(text = "Delete?")  
        layout.add_widget(popupLabel) 
        layout.add_widget(closeButton)
        layout.add_widget(okButton)
        #okButton.bind(on_press = self.onButtonPress) 
        # Instantiate the modal popup and display 

        popup = Popup(title = 'Danger of data loss', 
                    content = layout, 
                    size_hint =(None, None), size =(500, 200))   
          
        # Attach close button press with popup.dismiss action 
        closeButton.bind(on_press = popup.dismiss)
        okButton.bind(on_press =self.removed) 
        okButton.bind(on_press = popup.dismiss)
        popup.open()  

class Credits(Screen):
    pass
#------------instance of ScrenManager ---------------#######   
class ScreenManager(ScreenManager):
    pass

#--load gui.kv gui
# ---use open end encoding to utf8 ptbr
GUI = Builder.load_string(open("gui.kv", encoding="utf-8").read())
                      
#--main app
class MyApp(App):

    icon = 'icons/ico.png'
    title ='Mask detector'
    
    
    def build(self):
               
        return GUI
      
if __name__ == "__main__":

    MyApp().run()
    