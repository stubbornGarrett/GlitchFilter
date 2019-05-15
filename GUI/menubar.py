import tkinter as tk
#from tkinter import ttk

class Menubar(tk.Menu):
    def __init__(self, master, parent):
       tk.Menu.__init__(self, master)
       master.config(menu=self)

       self.create_widgets(parent)
       

    def create_widgets(self, parent):
        #Top Menu ******************************
        self.fileMenu = tk.Menu(self, tearoff=0)
        self.helpMenu = tk.Menu(self, tearoff=0)

        #File
        self.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Open Image')#, accelerator='Ctrl+O', command=self.browse_file)
        self.fileMenu.add_command(label='Save')#, accelerator='Ctrl+S', command=self.save_image)
        self.fileMenu.add_command(label='Save Image as...')#, accelerator='Ctrl+Alt+S', command=self.save_image_as)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=parent.quit_application)
       
        #bind_all('<Control-o>', self.browse_file)
        #bind_all('<Control-s>', self.save_image)
        #bind_all('<Control-Alt-s>', self.save_image_as)

        #Help
        self.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='About')#, command=open_about_window)