from PIL import Image, ImageChops
from tkinter import IntVar, StringVar
from tkinter.ttk import Frame, Label, Button, Entry, Checkbutton, Separator, Spinbox, Scale
from copy import copy
from random import random, randint, seed

unicodeSymbols = [u'\u21bb']

class BigBlocksFilter():
    def __init__(self, parent, master):
        self.master = master
        self.parent = parent

        self.name = 'Big Blocks Offset'

        self.create_parameters()
        self.create_widgets(parent)

    def create_parameters(self):
        #BigBlocksOffsetFilter parameters
        self.blockCountVar      = IntVar()
        self.blockCountVar.set(3)
        self.blockMaxHeightVar  = IntVar()
        self.blockMaxHeightVar.set(1)
        self.blockMaxOffsetVar  = IntVar()
        self.blockMaxOffsetVar.set(10)

        self.seedVar            = IntVar()
        self.seedVar.set(int(randint(0, 99999)))

        self.activeState        = IntVar()
        self.activeState.set(1)

    def create_widgets(self, parent):
        self.mainFrame      = parent
        self.cageFrame      = Frame(self.mainFrame)

        self.topFrame                   = Frame(self.cageFrame)

        self.blockCountLabel            = Label(    self.topFrame, text='Block Count', anchor='w')
        self.blockCountSpinbox          = Spinbox(  self.topFrame, from_=0, to_=30, textvariable=self.blockCountVar,        justify='right', width=6, command=self.update_widgets_config)#, command=self.update_parameters)
        self.blockMaxHeightLabel        = Label(    self.topFrame, text='Max Block Height (px)', anchor='w')
        self.blockMaxHeightSpinbox      = Spinbox(  self.topFrame, from_=0, to_=1,  textvariable=self.blockMaxHeightVar,    justify='right', width=6)#, command=self.update_widgets_config)#, command=self.update_parameters)
        
        self.blockMaxOffsetFrame        = Frame(    self.topFrame)
        self.blockMaxOffsetLabel        = Label(    self.blockMaxOffsetFrame, text='Max Offset (%)', anchor='w')
        self.blockMaxOffsetSpinbox      = Spinbox(  self.blockMaxOffsetFrame, from_=0, to_=100, textvariable=self.blockMaxOffsetVar,   justify='right', width=6)
        self.blockMaxOffsetScale        = Scale(    self.blockMaxOffsetFrame, from_=0, to_=100, variable=self.blockMaxOffsetVar, orient='horizontal', command=lambda s:self.blockMaxOffsetVar.set('%0.0f' % float(s)))

        self.seedFrame                  = Frame(    self.cageFrame)
        self.seedLabel                  = Label(    self.seedFrame, text='Seed (0 - 99999)', anchor='w')
        self.seedSpinbox                = Spinbox(  self.seedFrame, from_=0, to_=99999, textvariable=self.seedVar,           justify='right', width=6)
        self.randomSeedButton           = Button(   self.seedFrame, text=unicodeSymbols[0], command=lambda:self.seedVar.set(randint(0,99999))) #, font=('Arial', '13', 'bold')
        
        try:
            self.blockCountSpinbox.config(    font=self.master.mainWindow.defaultFont)
            self.blockMaxHeightSpinbox.config(font=self.master.mainWindow.defaultFont)
            self.blockMaxOffsetSpinbox.config(font=self.master.mainWindow.defaultFont)
            self.seedSpinbox.config(          font=self.master.mainWindow.defaultFont)
        except:
            pass

    def display_widgets(self):
        self.cageFrame.grid(column=0, row=0, sticky='we', padx=3)
        self.cageFrame.columnconfigure(0, weight=1)
        self.cageFrame.columnconfigure(1, weight=0)
        #self.mainFrame.columnconfigure(2, weight=1)
        self.cageFrame.rowconfigure(0, weight=0)
        self.cageFrame.rowconfigure(1, weight=0)#, pad=20)
        #self.mainFrame.rowconfigure(2, weight=1)

        self.topFrame.grid(             column=0, row=0, sticky='nwe')
        self.topFrame.columnconfigure(0, weight=1)
        self.topFrame.columnconfigure(1, weight=0)

        self.blockCountLabel.grid(      column=0, row=0, sticky='we', pady=3)
        self.blockCountSpinbox.grid(    column=1, row=0, sticky='w')
        self.blockMaxHeightLabel.grid(  column=0, row=1, sticky='we', pady=3)
        self.blockMaxHeightSpinbox.grid(column=1, row=1, sticky='w')

        self.blockMaxOffsetFrame.grid(  column=0, row=2, sticky='we', pady=3, columnspan=2)
        self.blockMaxOffsetFrame.columnconfigure(0, weight=1)
        self.blockMaxOffsetFrame.columnconfigure(1, weight=0)
        self.blockMaxOffsetLabel.grid(  column=0, row=0, sticky='we')
        self.blockMaxOffsetSpinbox.grid(column=1, row=0, sticky='w')
        self.blockMaxOffsetScale.grid(  column=0, row=1, sticky='we', columnspan=2)

        self.seedFrame.grid(            column=0, row=3, sticky='we', pady=10)
        self.seedFrame.columnconfigure(0, weight=0)
        self.seedFrame.columnconfigure(1, weight=0)
        self.seedFrame.columnconfigure(2, weight=0)
        self.seedLabel.grid(            column=0, row=0, sticky='we')
        self.randomSeedButton.grid(     column=1, row=0, sticky='w')
        self.seedSpinbox.grid(          column=2, row=0, sticky='e')

    def random_values(self):
        self.blockCountVar.set(randint(1, 3))
        self.seedVar.set(int(randint(0, 99999)))
        self.update_widgets_config()

    def update_widgets_config(self):
        maxHeight = int(( (self.master.mainWindow.sourceImage.height) / 100) * (100/self.blockCountVar.get()))
        self.blockMaxHeightSpinbox.config(to_=maxHeight)
        self.blockMaxHeightVar.set(maxHeight)

    def applyFilter(self, image):
        if self.activeState.get():
            print(self.name, ': started')
            seed(self.seedVar.get())
            sourceImage = copy(image)
            sourceImage.load()
            width, height = sourceImage.size
            size = width, height

            image = copy(sourceImage)

            x = 0
            while(x < self.blockCountVar.get()):
                #Define height and top edge (and bottom edge) of chunk
                randomHeight    = randint(int((self.blockMaxHeightVar.get()/100)*10), int(self.blockMaxHeightVar.get()))
                randYtop        = randint(x * self.blockMaxHeightVar.get()          , x * self.blockMaxHeightVar.get() + randomHeight)
                randYbottom     = randYtop + randomHeight

                #Cut chunk with predefined values
                tempCrop = sourceImage.crop((0, randYtop, width, randYbottom))

                #Generate random offset value and apply transposed chunk 
                if(random() > 0.5):
                    randXoffset =  randint(0, int((width/100) * self.blockMaxOffsetVar.get()))
                    image.paste(tempCrop, (randXoffset        , randYtop))
                    image.paste(tempCrop, (randXoffset - width, randYtop))
                else:
                    randXoffset = -randint(0, int((width/100) * self.blockMaxOffsetVar.get()))
                    image.paste(tempCrop, (randXoffset        , randYtop))
                    image.paste(tempCrop, (randXoffset + width, randYtop))
                x += 1

            seed()   #Randomize seed
            print('Big Blocks Filter: finished')
        return image