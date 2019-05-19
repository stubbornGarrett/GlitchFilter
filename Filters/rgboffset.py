from PIL import Image, ImageChops
from tkinter import IntVar, StringVar
from tkinter.ttk import Frame, Label, Button, Entry, Checkbutton, Separator
from copy import copy
from random import randint

class RGBoffsetFilter():
    def __init__(self, parent, master):
        self.master = master
        self.parent = parent

        self.name = 'RGB Offset'

        self.create_parameters()
        self.create_widgets(parent)
        self.mainFrame.columnconfigure(0, weight=0)
        self.mainFrame.columnconfigure(1, weight=0)
        self.mainFrame.columnconfigure(2, weight=0)
        self.mainFrame.rowconfigure(0, weight=0)
        self.mainFrame.rowconfigure(1, weight=0, pad=20)
        self.mainFrame.rowconfigure(2, weight=1)

    def create_parameters(self):
        #RGBoffsetFilter parameters
        self.RedXvar     = IntVar()
        self.RedXvar.set(5)
        self.RedYvar     = IntVar()
        self.RedYvar.set(5)
        self.GreenXvar   = IntVar()
        self.GreenXvar.set(-5)
        self.GreenYvar   = IntVar()
        self.GreenYvar.set(5)
        self.BlueXvar    = IntVar()
        self.BlueXvar.set(5)
        self.BlueYvar    = IntVar()
        self.BlueYvar.set(-5)

        self.nicerCheckButtonState = IntVar()
        self.nicerCheckButtonState.set(1)
        self.activeState = IntVar()
        self.activeState.set(1)

    def create_widgets(self, parent):
        self.mainFrame      = parent

        self.topFrame       = Frame(self.mainFrame)

        self.RedXlabel      = Label(self.topFrame, text='Red X\t(px)')
        self.RedXentry      = Entry(self.topFrame, textvariable=self.RedXvar,   justify='right', width=6, font=self.master.master.master.GlitchStyle.defaultFont)
        self.GreenXlabel    = Label(self.topFrame, text='Green X\t(px)')
        self.GreenXentry    = Entry(self.topFrame, textvariable=self.GreenXvar, justify='right', width=6, font=self.master.master.master.GlitchStyle.defaultFont)
        self.BlueXlabel     = Label(self.topFrame, text='Blue X\t(px)')
        self.BlueXentry     = Entry(self.topFrame, textvariable=self.BlueXvar,  justify='right', width=6, font=self.master.master.master.GlitchStyle.defaultFont)
        self.RedYlabel      = Label(self.topFrame, text='Red Y\t(px)')
        self.RedYentry      = Entry(self.topFrame, textvariable=self.RedYvar,   justify='right', width=6, font=self.master.master.master.GlitchStyle.defaultFont)
        self.GreenYlabel    = Label(self.topFrame, text='Green Y\t(px)')
        self.GreenYentry    = Entry(self.topFrame, textvariable=self.GreenYvar, justify='right', width=6, font=self.master.master.master.GlitchStyle.defaultFont)
        self.BlueYlabel     = Label(self.topFrame, text='Blue Y\t(px)')
        self.BlueYentry     = Entry(self.topFrame, textvariable=self.BlueYvar,  justify='right', width=6, font=self.master.master.master.GlitchStyle.defaultFont)

        self.frameSeperator = Separator(self.mainFrame)
       
        self.bottomFrame        = Frame(        self.mainFrame)
        self.nicerCheckbutton   = Checkbutton(  self.bottomFrame, text='Nicer Values',  variable=self.nicerCheckButtonState)
        self.RandomButton       = Button(       self.bottomFrame, text='Random Values', command=self.random_values)

    def display_widgets(self):
        self.topFrame.grid(     column=0, row=0, sticky='we')
        self.topFrame.columnconfigure(0, weight=1)
        self.topFrame.columnconfigure(1, weight=0)

        self.RedXlabel.grid(    column=0, row=0, sticky='we')
        self.RedXentry.grid(    column=1, row=0, sticky='w')
        self.RedYlabel.grid(    column=0, row=1, sticky='we')
        self.RedYentry.grid(    column=1, row=1, sticky='w')
        self.GreenXlabel.grid(  column=0, row=2, sticky='we')
        self.GreenXentry.grid(  column=1, row=2, sticky='w')
        self.GreenYlabel.grid(  column=0, row=3, sticky='we')
        self.GreenYentry.grid(  column=1, row=3, sticky='w')
        self.BlueXlabel.grid(   column=0, row=4, sticky='we')
        self.BlueXentry.grid(   column=1, row=4, sticky='w')
        self.BlueYlabel.grid(   column=0, row=5, sticky='we')
        self.BlueYentry.grid(   column=1, row=5, sticky='w')
        
        self.frameSeperator.grid(column=0, row=1, sticky='we')

        self.bottomFrame.grid(          column=0, row=2, sticky='nwe')
        self.bottomFrame.columnconfigure(0, weight=1)
        self.bottomFrame.columnconfigure(1, weight=1)
        self.nicerCheckbutton.grid(     column=0, row=0, sticky='w')
        self.RandomButton.grid(         column=1, row=0, sticky='we')

    def random_values(self):
        if self.nicerCheckButtonState.get():
            valueX = int((self.master.master.master.sourceImage.width  / 100) * 0.3)
            valueY = int((self.master.master.master.sourceImage.height / 100) * 0.3)
            
            self.RedXvar.set(   randint(-valueX, valueX))
            self.RedYvar.set(   randint(-valueY, valueY))
            self.GreenXvar.set( randint(-valueX, valueX))
            self.GreenYvar.set( randint(-valueY, valueY))
            self.BlueXvar.set(  randint(-valueX, valueX))
            self.BlueYvar.set(  randint(-valueY, valueY))
        
        else:
            width  = self.master.master.master.sourceImage.width
            height = self.master.master.master.sourceImage.height
            self.RedXvar.set(   randint(-width,  width))
            self.RedYvar.set(   randint(-height, height))
            self.GreenXvar.set( randint(-width,  width))
            self.GreenYvar.set( randint(-height, height))
            self.BlueXvar.set(  randint(-width,  width))
            self.BlueYvar.set(  randint(-height, height))

            print(self.RedXvar)

    def update_widgets_config(self, event=None):
        pass

    def applyFilter(self, image):
        if self.activeState.get():
            print('RGB Offset Filter: started')
            #Create Variables
            sourceImage = copy(image)
            #sourceData   = sourceImage.getdata()
            width, height = sourceImage.size
            size        = width, height

            #Create temporary Images
            finishedImage = Image.new('RGB', size)

            redImage    = Image.new('RGB', size)
            greenImage  = Image.new('RGB', size)
            blueImage   = Image.new('RGB', size)

            #Split RGB channels 
            r, g, b       = sourceImage.split()      #RGB Channels of the source Image
            rNu, gNu, bNu = finishedImage.split()    #'RGB' Channels of the generated Image -> all black 

            #Create an Image for every channel (merge colored and black channels)
            redImage    = Image.merge('RGB' , (r, gNu, bNu))
            greenImage  = Image.merge('RGB' , (rNu, g, bNu))
            blueImage   = Image.merge('RGB' , (rNu, gNu, b))
 
            #Offsets every temporary Image by values given from user
            redImage    = ImageChops.offset(redImage,   self.RedXvar.get(),      self.RedYvar.get())
            greenImage  = ImageChops.offset(greenImage, self.GreenXvar.get(),    self.GreenYvar.get())
            blueImage   = ImageChops.offset(blueImage,  self.BlueXvar.get(),     self.BlueYvar.get())

            #Again splits the RGB channels of the temporary Images
            r, gNu, bNu = redImage.split()
            rNu, g, bNu = greenImage.split()
            rNu, gNu, b = blueImage.split()

            #Merge them to final Image
            finishedImage      = Image.merge('RGB', (r, g, b))
            finishedImage.load()

            print('RGB Offset Filter: finished')
            return finishedImage