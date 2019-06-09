from PIL import Image, ImageChops
from tkinter import IntVar, StringVar
from tkinter.ttk import Frame, Label, Button, Spinbox, Checkbutton, Separator
from copy import copy
from random import randint

class RGBoffsetFilter():
    def __init__(self, parent, master):
        self.master = master
        self.parent = parent

        self.name = 'RGB Offset'

        self.create_parameters()
        self.create_widgets(parent)

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
        self.cageFrame      = Frame(self.mainFrame)

        self.topFrame       = Frame(self.cageFrame)

        validation = (self.master.master.master.register(self.validate_input), '%S', '%P')
        self.RedXlabel      = Label(    self.topFrame, text='Red X\t(px)')
        self.RedXspinbox    = Spinbox(  self.topFrame, textvariable=self.RedXvar,   justify='right', width=6, from_=-1920, to_=1920, validate='key', validatecomman=validation)
        self.GreenXlabel    = Label(    self.topFrame, text='Green X\t(px)')
        self.GreenXspinbox  = Spinbox(  self.topFrame, textvariable=self.GreenXvar, justify='right', width=6, from_=-1920, to_=1920)
        self.BlueXlabel     = Label(    self.topFrame, text='Blue X\t(px)')
        self.BlueXspinbox   = Spinbox(  self.topFrame, textvariable=self.BlueXvar,  justify='right', width=6, from_=-1920, to_=1920)
        self.RedYlabel      = Label(    self.topFrame, text='Red Y\t(px)')
        self.RedYspinbox    = Spinbox(  self.topFrame, textvariable=self.RedYvar,   justify='right', width=6, from_=-1920, to_=1920)
        self.GreenYlabel    = Label(    self.topFrame, text='Green Y\t(px)')
        self.GreenYspinbox  = Spinbox(  self.topFrame, textvariable=self.GreenYvar, justify='right', width=6, from_=-1920, to_=1920)
        self.BlueYlabel     = Label(    self.topFrame, text='Blue Y\t(px)')
        self.BlueYspinbox   = Spinbox(  self.topFrame, textvariable=self.BlueYvar,  justify='right', width=6, from_=-1920, to_=1920)

        try:
            self.RedXspinbox.config(  font=self.master.mainWindow.defaultFont)
            self.GreenXspinbox.config(font=self.master.mainWindow.defaultFont)
            self.BlueXspinbox.config( font=self.master.mainWindow.defaultFont)
            self.RedYspinbox.config(  font=self.master.mainWindow.defaultFont)
            self.GreenYspinbox.config(font=self.master.mainWindow.defaultFont)
            self.BlueYspinbox.config( font=self.master.mainWindow.defaultFont)
        except:
            pass

        self.frameSeperator = Separator(self.cageFrame)
       
        self.bottomFrame        = Frame(        self.cageFrame)
        self.nicerCheckbutton   = Checkbutton(  self.bottomFrame, text='Nicer Values',  variable=self.nicerCheckButtonState)
        self.RandomButton       = Button(       self.bottomFrame, text='Random Values', command=self.random_values)

    def display_widgets(self):
        self.mainFrame.columnconfigure( 0, weight=1)
        self.mainFrame.rowconfigure(    0, weight=1)

        self.cageFrame.grid(    column=0, row=0, sticky='we', padx=3)
        self.cageFrame.columnconfigure(0, weight=1)#, pad=10)
        self.cageFrame.columnconfigure(1, weight=0)
        self.cageFrame.columnconfigure(2, weight=0)
        self.cageFrame.rowconfigure(0, weight=0)
        self.cageFrame.rowconfigure(1, weight=0, pad=15)
        self.cageFrame.rowconfigure(2, weight=0)

        self.topFrame.grid(     column=0, row=0, sticky='we')
        self.topFrame.columnconfigure(0, weight=1)
        self.topFrame.columnconfigure(1, weight=0)

        self.RedXlabel.grid(    column=0, row=0, sticky='we', pady=3)
        self.RedXspinbox.grid(  column=1, row=0, sticky='w')
        self.RedYlabel.grid(    column=0, row=1, sticky='we', pady=3)
        self.RedYspinbox.grid(  column=1, row=1, sticky='w')
        self.GreenXlabel.grid(  column=0, row=2, sticky='we', pady=3)
        self.GreenXspinbox.grid(column=1, row=2, sticky='w')
        self.GreenYlabel.grid(  column=0, row=3, sticky='we', pady=3)
        self.GreenYspinbox.grid(column=1, row=3, sticky='w')
        self.BlueXlabel.grid(   column=0, row=4, sticky='we', pady=3)
        self.BlueXspinbox.grid( column=1, row=4, sticky='w')
        self.BlueYlabel.grid(   column=0, row=5, sticky='we', pady=3)
        self.BlueYspinbox.grid( column=1, row=5, sticky='w')
        
        self.frameSeperator.grid(column=0, row=1, sticky='we')

        self.bottomFrame.grid(          column=0, row=2, sticky='we')
        self.bottomFrame.columnconfigure(0, weight=0)
        self.bottomFrame.columnconfigure(1, weight=1)
        self.nicerCheckbutton.grid(     column=0, row=0, sticky='w')
        self.RandomButton.grid(         column=1, row=0, sticky='we')

    def random_values(self):
        if self.activeState.get():
            if self.nicerCheckButtonState.get():
                valueX = int((self.master.mainWindow.sourceImage.width  / 100) * 0.3)
                valueY = int((self.master.mainWindow.sourceImage.height / 100) * 0.3)

                self.RedXvar.set(   randint(-valueX, valueX))
                self.RedYvar.set(   randint(-valueY, valueY))
                self.GreenXvar.set( randint(-valueX, valueX))
                self.GreenYvar.set( randint(-valueY, valueY))
                self.BlueXvar.set(  randint(-valueX, valueX))
                self.BlueYvar.set(  randint(-valueY, valueY))

            else:
                width  = self.master.mainWindow.sourceImage.width
                height = self.master.mainWindow.sourceImage.height
                self.RedXvar.set(   randint(-width,  width))
                self.RedYvar.set(   randint(-height, height))
                self.GreenXvar.set( randint(-width,  width))
                self.GreenYvar.set( randint(-height, height))
                self.BlueXvar.set(  randint(-width,  width))
                self.BlueYvar.set(  randint(-height, height))

    def update_widgets_config(self, event=None):
        if self.activeState.get():
            pass

    def validate_input(self, input, result):
        print(result)
        if input.isdigit() and self.master.mainWindow.sourceImage.height*2 > int(result):
            return True
        else:
            return False

    def applyFilter(self, image):
        if self.activeState.get():
            print(self.name, ': started')
            #Create Variables
            sourceImage = copy(image)
            width, height = sourceImage.size
            size        = width, height

            #Create temporary Images
            blackImage = Image.new('RGB', size)

            redImage    = Image.new('RGB', size)
            greenImage  = Image.new('RGB', size)
            blueImage   = Image.new('RGB', size)

            #Split RGB channels 
            r, g, b       = sourceImage.split()   #RGB Channels of the source Image
            rNu, gNu, bNu = blackImage.split()    #'RGB' Channels of the generated Image -> all black 
            del blackImage

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
            image       = Image.merge('RGB', (r, g, b))
            #image.load()

            print('RGB Offset Filter: finished')
        return image