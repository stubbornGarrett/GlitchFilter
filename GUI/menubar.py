import tkinter as tk
import os
import copy
from tkinter.filedialog import askopenfilename
from tools import logger
from PIL import Image, ImageTk
#from tkinter import ttk

class Menubar(tk.Menu):
    def __init__(self, master, parent):
        tk.Menu.__init__(self, master)
        master.config(menu=self)
        self.parent = parent

        self.create_widgets(parent)
       

    def create_widgets(self, parent):
        #Top Menu ******************************
        self.fileMenu = tk.Menu(self, tearoff=0)
        self.helpMenu = tk.Menu(self, tearoff=0)

        #File
        self.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Open Image', accelerator='Ctrl+O', command=self.open_image)
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

    def open_image(self):
        tempSourceImagePath = ''
        tempSourceImagePath = askopenfilename(initialdir='/', title='Open Image...', defaultextension=self.parent.sourceImageExtension, **self.parent.FILEOPTIONS)

        if tempSourceImagePath: # and self.continue_without_save():
            try:
                filename, self.parent.sourceImageExtension = os.path.splitext(tempSourceImagePath)
                del filename
                self.parent.sourceImagePath = tempSourceImagePath
                self.parent.sourceImage = Image.open(self.parent.sourceImagePath)
                self.parent.sourceImage.load()
                self.parent.tempImage = copy.copy(self.parent.sourceImage)
            except:
                logger.log.exception('Loading Image failed! - Filepath: ', tempSourceImagePath)
                #showerror('Error', 'Loading Image failed! - Filepath:\n{}'.format(tempSourceImagePath))
                self.parent.sourceImagePath = ''
            else:
                self.parent.firstImageLoaded = True
                self.parent.imagepreviewWidget.sizeMultiplicator = 1.0
                self.parent.imagepreviewWidget.display_image(self.parent.tempImage)
                #self.sourceImage.load()
                #self.firstImageLoaded = True
                #self.sourceImage = self.sourceImage.convert('RGB')
                #self.tempImage = copy.deepcopy(self.sourceImage)