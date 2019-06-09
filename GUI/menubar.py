from tools import logger
import tkinter as tk
import os
from copy import copy
from tkinter.messagebox import showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename, asksaveasfile
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
        self.add_cascade(label='File', underline=0, menu=self.fileMenu)
        self.fileMenu.add_command(label='Open Image', underline=0, accelerator='Ctrl+O', command=self.open_image)#, font=self.mainWindow.defaultFont)
        self.fileMenu.add_command(label='Save', accelerator='Ctrl+S', command=self.save_image)
        self.fileMenu.add_command(label='Save Image as...', accelerator='Ctrl+Shift+S', command=self.save_image_as)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Close Image', accelerator='Ctrl+Shift+X', command=self.close_image)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=mainWindow.quit_application)

        self.bind_all('<Control-o>', self.open_image)
        self.bind_all('<Control-s>', self.save_image)
        self.bind_all('<Control-Shift-KeyPress-S>', self.save_image_as)
        self.bind_all('<Control-Shift-KeyPress-X>', self.close_image)

        #Help Menu
        # self.add_cascade(label='Help', menu=self.helpMenu)
        # self.helpMenu.add_command(label='About')#, command=open_about_window)

    def open_image(self, event=None):
        tempSourceImagePath = ''
        tempSourceImagePath = askopenfilename(title='Open Image...', defaultextension='.', filetypes=self.mainWindow.filetypes) # initialdir='/', 

        if tempSourceImagePath and self.mainWindow.continue_without_save():
            try:
                self.mainWindow.sourceImage = Image.open(tempSourceImagePath)
                self.mainWindow.sourceImage.load()

                self.mainWindow.sourceImagePath                                         = os.path.dirname(tempSourceImagePath)
                fileNameAndExtension                                                    = os.path.basename(tempSourceImagePath)
                self.mainWindow.sourceImageName, self.mainWindow.sourceImageExtension   = os.path.splitext(fileNameAndExtension)

                #self.mainWindow.sourceImage     = self.mainWindow.sourceImage.convert('RGB')
                self.mainWindow.tempImage   = copy(self.mainWindow.sourceImage)
            except:
                logger.log.exception('Loading Image failed! - Filepath: ', tempSourceImagePath)
                showerror('Error', 'Loading Image failed! - Filepath:\n{}'.format(tempSourceImagePath))
                self.mainWindow.sourceImagePath     = ''
                self.mainWindow.imageIsLoaded       = False
                self.mainWindow.tempImage           = None
                self.mainWindow.sourceImage         = None
            else:
                self.mainWindow.imageIsLoaded    = True
                self.mainWindow.imageIsSaved    = True
                self.mainWindow.imagepreviewWidget.update_image(self.mainWindow.sourceImage)
                self.mainWindow.imagepreviewWidget.reset_preview()
                self.mainWindow.infobarWidget.update_imageInfo(' Width: {}, Height: {}'.format(self.mainWindow.sourceImage.width, self.mainWindow.sourceImage.height))
                self.mainWindow.infobarWidget.update_previewInfo('x{}'.format(round(self.mainWindow.imagepreviewWidget.canvasScale,2)))

                for filter in self.mainWindow.configbarWidget.filterListObj:
                    filter.update_widgets_config()

    def save_image(self, event=None):
        if self.mainWindow.imageIsLoaded:
            try:
                self.mainWindow.tempImage.save('{}\{}{}{}'.format(self.mainWindow.sourceImagePath, self.mainWindow.sourceImageName, '-Glitch', self.mainWindow.sourceImageExtension))
            except:
                logger.log.exception('Saveing Image failed!')
                showerror('Error', 'Saveing Image failed! - Filepath:\n{}'.format('{}\{}{}{}'.format(self.mainWindow.sourceImagePath, self.mainWindow.sourceImageName, '-Glitch', self.mainWindow.sourceImageExtension)))
            else:
                self.mainWindow.imageIsSaved = True

    def save_image_as(self, event=None):
        if self.mainWindow.imageIsLoaded:
            tempFilePath = asksaveasfilename(initialdir='{}/'.format(self.mainWindow.sourceImagePath), title='Save Image...', defaultextension=self.mainWindow.sourceImageExtension, filetypes=self.mainWindow.filetypes)
        try:
            if tempFilePath:
                self.mainWindow.tempImage.save(tempFilePath)
                self.imageIsSaved = True
        except:
            logger.log.exception('Saveing Image failed!')
            showerror('Error', 'Saveing Image failed! - Filepath:\n{}'.format(tempFilePath))

    def close_image(self, event=None):
        if self.mainWindow.continue_without_save():
            self.mainWindow.imagepreviewWidget.update_image(image=None)
            self.mainWindow.imageIsSaved  = True
            self.mainWindow.imageIsLoaded = False