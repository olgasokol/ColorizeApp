from __future__ import print_function
import kivy
kivy.require('1.10.0') # replace with your current kivy version !

import os
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from functools import partial
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.modalview import ModalView
from kivy.uix.stacklayout import StackLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from forward import Colorizer
from skimage.io import imsave, imread


class ColorizeApp(App):

    def __init__(self):
        super().__init__()
        self.download_path = StringProperty('')
        self.file_chooser = FileChooserListView(dirselect = True)
        self.btn_ok = Button(size_hint_y=0.075,text="Select")
        self.content_pop_download = BoxLayout(orientation = 'vertical')
        self.content_pop_download.add_widget(self.file_chooser)
        self.content_pop_download.add_widget(self.btn_ok)
        self.pop_downloader = Popup(
            size_hint = (0.8,0.8),
            title="Choose file",
            content = self.content_pop_download,
            auto_dismiss=True)
    
    def colorize_click(self):
        print("starting coloring...")
        colorizer = Colorizer()
        str = colorizer.colorize(self.root.ids.in_img.source)
        self.root.ids.out_img.source=str
        print("loaded image to view")
		
    def build(self):
        str = os.path.realpath(__file__).replace('main.py','my.kv')
        #str = 'C:\\app_ui\\my.kv'
        return Builder.load_file(str)

    def load_f(self):
        self.btn_ok.bind(on_press=lambda x:self.get_file(x))
        self.pop_downloader.open()
        
    def get_file(self, button):
        download_path = self.file_chooser.selection[0]
        self.pop_downloader.dismiss()
        self.root.ids.in_img.source=download_path

    def save(self):
        old_name, format = self.root.ids.in_img.source.split('.')
        new_name = old_name + '_colorized.'+format
        imsave(new_name, imread(self.root.ids.out_img.source))
        save_popup = Popup(
            size_hint = (0.5,0.5),
            title="Choose file",
            content = Label(text="Image saved as "+new_name),
            auto_dismiss=True)
        save_popup.open()


if __name__ == '__main__':
    ColorizeApp().run()
