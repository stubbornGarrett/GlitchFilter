from tools import logger
import tkinter as tk
import os
from copy import copy
from tkinter.filedialog import askopenfilename, asksaveasfile
from tools import logger
from PIL import Image, ImageTk
#from tkinter import ttk

class Menubar(tk.Menu):
    def __init__(self, master, mainWindow): # master = root (Tk) | mainWindow = main Frame of application
        tk.Menu.__init__(self, master)
        master.config(menu=self)
        self.mainWindow = mainWindow

        self.create_widgets(mainWindow)

    def create_widgets(self, mainWindow):
        #Top Menu ******************************
        self.fileMenu = tk.Menu(self, tearoff=0)
        self.helpMenu = tk.Menu(self, tearoff=0)

        #File Menu
        self.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Open Image', accelerator='Ctrl+O', command=self.open_image)
        self.fileMenu.add_command(label='Save', accelerator='Ctrl+S', command=self.save_image)
        self.fileMenu.add_command(label='Save Image as...')#, accelerator='Ctrl+Alt+S', command=self.save_image_as)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=mainWindow.quit_application)

        self.bind_all('<Control-o>', self.open_image)
        self.bind_all('<Control-s>', self.save_image)
        #bind_all('<Control-Alt-s>', self.save_image_as)

        #Help Menu
        self.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='About')#, command=open_about_window)

    def open_image(self, event=None):
        tempSourceImagePath = ''
        tempSourceImagePath = askopenfilename(title='Open Image...', defaultextension='.', filetypes=self.mainWindow.filetypes) # initialdir='/', 

        if tempSourceImagePath: # and self.continue_without_save():
            try:
                self.mainWindow.sourceImage             = Image.open(tempSourceImagePath)
                self.mainWindow.sourceImage.load()

                self.mainWindow.sourceImagePath                                         = os.path.dirname(tempSourceImagePath)
                fileNameAndExtension                                                    = os.path.basename(tempSourceImagePath)
                self.mainWindow.sourceImageName, self.mainWindow.sourceImageExtension   = os.path.splitext(fileNameAndExtension)

                #self.mainWindow.sourceImage     = self.mainWindow.sourceImage.convert('RGB')
                self.mainWindow.tempImage               = copy(self.mainWindow.sourceImage)
                self.mainWindow.sourceImageThumbnail    = self.create_thumbnail(self.mainWindow.sourceImage)
                self.mainWindow.tempImageThumbnail      = self.mainWindow.sourceImageThumbnail
            except:
                logger.log.exception('Loading Image failed! - Filepath: ', tempSourceImagePath)
                #showerror('Error', 'Loading Image failed! - Filepath:\n{}'.format(tempSourceImagePath))
                self.mainWindow.sourceImagePath = ''
            else:
                self.mainWindow.firstImageLoaded    = True
                self.mainWindow.sizeMultiplicator   = 1.0
                self.mainWindow.previewXoffset      = 0
                self.mainWindow.previewYoffset      = 0
                self.mainWindow.imagepreviewWidget.adjust_canvas_size(event=None)

                for filter in self.mainWindow.configbarWidget.filterListObj:
                    filter.update_widgets_config()

                #self.sourceImage.load()
                #self.firstImageLoaded = True
                #self.sourceImage = self.sourceImage.convert('RGB')
                #self.tempImage = copy.deepcopy(self.sourceImage)

    def save_image(self, event=None):
        if self.mainWindow.firstImageLoaded:
            self.mainWindow.tempImage.save('{}{}{}{}'.format(self.mainWindow.sourceImagePath, self.mainWindow.sourceImageName, '-Glitch', self.mainWindow.sourceImageExtension))

    def create_thumbnail(self, image):
        if image.width > self.mainWindow.imagepreviewWidget.previewCanvas.winfo_width() or image.height > self.mainWindow.imagepreviewWidget.previewCanvas.winfo_height():
            if image.height > self.master.winfo_screenheight():
                scale = self.master.winfo_screenheight() / image.height
                image = image.resize((int(image.width * scale), int(image.height * scale)), resample=Image.LANCZOS)
            if image.width > self.master.winfo_screenwidth():
                scale = self.master.winfo_screenwidth() / image.width
                image = image.resize((int(image.width * scale), int(image.height * scale)), resample=Image.LANCZOS)
        print('Created thumbnail!')
        return image