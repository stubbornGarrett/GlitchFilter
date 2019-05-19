from tools import logger
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

        #File Menu
        self.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Open Image', accelerator='Ctrl+O', command=self.open_image)
        self.fileMenu.add_command(label='Save')#, accelerator='Ctrl+S', command=self.save_image)
        self.fileMenu.add_command(label='Save Image as...')#, accelerator='Ctrl+Alt+S', command=self.save_image_as)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=parent.quit_application)
       
        self.bind_all('<Control-o>', self.open_image)
        #bind_all('<Control-s>', self.save_image)
        #bind_all('<Control-Alt-s>', self.save_image_as)

        #Help Menu
        self.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='About')#, command=open_about_window)

    def open_image(self, event=None):
        tempSourceImagePath = ''
        tempSourceImagePath = askopenfilename(initialdir='/', title='Open Image...', defaultextension=self.parent.sourceImageExtension, **self.parent.FILEOPTIONS)

        if tempSourceImagePath: # and self.continue_without_save():
            try:
                filename, self.parent.sourceImageExtension = os.path.splitext(tempSourceImagePath)
                del filename
                self.parent.sourceImagePath = tempSourceImagePath
                self.parent.sourceImage     = Image.open(self.parent.sourceImagePath)
                #self.parent.sourceImage     = self.parent.sourceImage.convert('RGB')
                self.parent.sourceImage.load()
                self.parent.tempImage       = copy.copy(self.parent.sourceImage)
                self.parent.sourceImageThumbnail    = self.create_thumbnail(self.parent.sourceImage)
                self.parent.tempImageThumbnail      = copy.copy(self.parent.sourceImageThumbnail)
            except:
                logger.log.exception('Loading Image failed! - Filepath: ', tempSourceImagePath)
                #showerror('Error', 'Loading Image failed! - Filepath:\n{}'.format(tempSourceImagePath))
                self.parent.sourceImagePath = ''
            else:
                self.parent.firstImageLoaded    = True
                self.parent.sizeMultiplicator   = 1.0
                self.parent.previewXoffset      = 0
                self.parent.previewYoffset      = 0
                self.parent.imagepreviewWidget.adjust_canvas_size(event=None)

                for filter in self.parent.configbarWidget.filterListObj:
                    filter.update_widgets_config()

                #self.parent.configbarWidget.bigblocksFilter.update_widgets_config()
                
                #self.sourceImage.load()
                #self.firstImageLoaded = True
                #self.sourceImage = self.sourceImage.convert('RGB')
                #self.tempImage = copy.deepcopy(self.sourceImage)

    def create_thumbnail(self, image):
        if image.width > self.parent.imagepreviewWidget.previewCanvas.winfo_width() or image.height > self.parent.imagepreviewWidget.previewCanvas.winfo_height():
            if image.height > self.master.winfo_screenheight():
                scale = self.master.winfo_screenheight() / image.height
                image = image.resize((int(image.width * scale), int(image.height * scale)), resample=Image.LANCZOS)
            if image.width > self.master.winfo_screenwidth():
                scale = self.master.winfo_screenwidth() / image.width
                image = image.resize((int(image.width * scale), int(image.height * scale)), resample=Image.LANCZOS)
        print('Created thumbnail!')
        return image