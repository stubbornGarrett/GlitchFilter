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
        self.mainFrame.columnconfigure(0, weight=0)
        self.mainFrame.columnconfigure(1, weight=0)
        self.mainFrame.columnconfigure(2, weight=1)
        #self.mainFrame.rowconfigure(0, weight=0)
        #self.mainFrame.rowconfigure(1, weight=0, pad=20)
        #self.mainFrame.rowconfigure(2, weight=1)

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

        self.topFrame                   = Frame(self.mainFrame)

        self.blockCountLabel            = Label(    self.topFrame, text='Block Count', anchor='w')
        self.blockCountSpinbox          = Spinbox(  self.topFrame, from_=0, to_=20, textvariable=self.blockCountVar,        justify='right', width=6, font=self.master.master.master.GlitchStyle.defaultFont, command=self.update_widgets_config)#, command=self.update_parameters)
        self.blockMaxHeightLabel        = Label(    self.topFrame, text='Max Block Height (px)', anchor='w')
        self.blockMaxHeightSpinbox      = Spinbox(  self.topFrame, from_=0, to_=1, textvariable=self.blockMaxHeightVar,     justify='right', width=6, font=self.master.master.master.GlitchStyle.defaultFont, command=self.update_widgets_config)#, command=self.update_parameters)
        self.blockMaxOffsetLabel        = Label(    self.topFrame, text='Max Offset (%)', anchor='w')
        self.blockMaxOffsetSpinbox      = Spinbox(  self.topFrame, from_=0, to_=100, textvariable=self.blockMaxOffsetVar,   justify='right', width=6, font=self.master.master.master.GlitchStyle.defaultFont)
        self.blockMaxOffsetScale        = Scale(    self.topFrame, from_=0, to_=100, variable=self.blockMaxOffsetVar, orient='horizontal', command=lambda s:self.blockMaxOffsetVar.set('%0.0f' % float(s)))
        self.seedLabel                  = Label(    self.topFrame, text='Seed (0 - 99999)', anchor='w')
        self.seedSpinbox                = Spinbox(  self.topFrame, from_=0, to_=99999, textvariable=self.seedVar,           justify='right', width=6, font=self.master.master.master.GlitchStyle.defaultFont)
        self.randomSeedButton           = Button(   self.topFrame, text=unicodeSymbols[0], command=lambda:self.seedVar.set(randint(0,99999))) #, font=('Arial', '13', 'bold')

    def random_values(self):
        self.blockCountVar.set(randint(1, 7))
        self.seedVar.set(int(randint(0, 99999)))
        self.update_widgets_config()

    def update_widgets_config(self):
        print('Started updateing widgets')
        print(self.master.master.master.sourceImage.height)
        maxHeight = int(( (self.master.master.master.sourceImage.height) / 100) * (100/self.blockCountVar.get()))
        self.blockMaxHeightSpinbox.config(to_=maxHeight)
        self.blockMaxHeightVar.set(maxHeight)
        print('Widgets updated')

    def display_widgets(self):
        self.topFrame.grid(             column=0, row=0, sticky='we')
        self.topFrame.columnconfigure(0, weight=0)
        self.topFrame.columnconfigure(1, weight=0)
        self.topFrame.columnconfigure(2, weight=1)

        self.blockCountLabel.grid(      column=0, row=0, sticky='we')
        self.blockCountSpinbox.grid(    column=1, row=0, sticky='w')
        self.blockMaxHeightLabel.grid(  column=0, row=1, sticky='we')
        self.blockMaxHeightSpinbox.grid(column=1, row=1, sticky='w')
        self.blockMaxOffsetLabel.grid(  column=0, row=2, sticky='we')
        self.blockMaxOffsetSpinbox.grid(column=1, row=2, sticky='w')
        self.blockMaxOffsetScale.grid(  column=2, row=2, sticky='we')

        self.seedLabel.grid(            column=0, row=3, sticky='we')
        self.seedSpinbox.grid(          column=1, row=3, sticky='w')
        self.randomSeedButton.grid(     column=2, row=3, sticky='w')

    def update_widgets_config(self):
        pass

    def applyFilter(self, image):
        if self.activeState.get():
            print('Big Blocks Filter: started')
            seed(self.seedVar.get())
            sourceImage = copy(image)
            sourceImage.load()
            width, height = sourceImage.size
            size = width, height

            finishedImage = copy(sourceImage)

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
                    finishedImage.paste(tempCrop, (randXoffset        , randYtop))
                    finishedImage.paste(tempCrop, (randXoffset - width, randYtop))
                else:
                    randXoffset = -randint(0, int((width/100) * self.blockMaxOffsetVar.get()))
                    finishedImage.paste(tempCrop, (randXoffset        , randYtop))
                    finishedImage.paste(tempCrop, (randXoffset + width, randYtop))
                x += 1

            finishedImage.load()
            seed()   #Randomize seed
            print('Big Blocks Filter: finished')
            return finishedImage