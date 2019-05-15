import tkinter as tk
import tkinter.ttk as ttk

class Imagepreview(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid(column=0, row=0, sticky='news')
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 0, weight=1)
        
    def display_image(self, image):
        pass