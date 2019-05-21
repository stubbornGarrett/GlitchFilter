from PIL import Image, ImageChops
from tkinter import IntVar, StringVar
from tkinter.ttk import Frame, Label, Button, Entry, Checkbutton, Separator
from copy import copy
from random import randint

class CLASSNAMEOFFILTER():  #Change Name!!!
    def __init__(self, parent, master):
        self.parent = parent #
        self.master = master

        self.name = '*******List name of Filter*******'

        self.create_parameters()
        self.create_widgets(parent)
        #self.mainFrame.columnconfigure(0, weight=0)
        #self.mainFrame.columnconfigure(1, weight=0)
        #self.mainFrame.columnconfigure(2, weight=0)
        #self.mainFrame.rowconfigure(0, weight=0)
        #self.mainFrame.rowconfigure(1, weight=0, pad=20)
        #self.mainFrame.rowconfigure(2, weight=1)

    def create_parameters(self):
        #Create filter parameters here
        self.activeState = IntVar()     #Controls if the filter gets applied
        self.activeState.set(1)

    def create_widgets(self, parent):
        self.mainFrame      = parent
		self.cageFrame		= Frame(self.mainFrame) # Parent of all widgets
        #Create widgets here (no .grid yet)
        #Attach them to 'mainFrame'

    def display_widgets(self):
        self.cageFrame.grid(column=0, row=0, sticky='we', padx=3)
        self.cageFrame.columnconfigure(0, weight=1)
        self.cageFrame.columnconfigure(1, weight=0)
        #Display widgets with .grid
        pass

    def random_values(self):
		if self.activeState.get():
			#Function gets executed, when 'Random Render' Button is hit
			pass

    def update_widgets_config(self, event=None):
		if self.activeState.get():
			#Everything what changes, if an other picture gets loaded
			#or when widgets update themselfe
			pass

    def applyFilter(self, image):
        if self.activeState.get():
            print('****Name of Filter****: started')
            #Create Variables
            sourceImage = copy(image)
            #sourceData   = sourceImage.getdata()
            width, height = sourceImage.size
            size        = width, height

            #*********************
            #Insert Algorithm here
            #*********************

			image = finishedImage

        return image