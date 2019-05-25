from PIL import Image, ImageChops, ImageFilter
from tkinter import IntVar, StringVar
from tkinter.ttk import Frame, Label, Button, Entry, Checkbutton, Separator, Spinbox, Scale
from copy import copy
from random import randint, seed
import numpy as np

unicodeSymbols = [u'\u21bb']

class BurningNoiseFilter():
    def __init__(self, parent, master):
        self.parent = parent 
        self.master = master

        self.name = 'Burning Noise'

        self.create_parameters()
        self.create_widgets(parent)

    def create_parameters(self):
        self.randomNoiseData = []

        self.pixelSizeVar       = IntVar()
        self.pixelSizeVar.set(  1)
        self.stretchWidthVar    = IntVar()
        self.stretchWidthVar.set(25)
        self.stretchHeightVar   = IntVar()
        self.stretchHeightVar.set(0)
        self.brightVar          = IntVar()
        self.brightVar.set(     150)
        self.darkVar            = IntVar()
        self.darkVar.set(       10)
        self.contrastVar        = IntVar()
        self.contrastVar.set(   0)
        self.intensityVar       = IntVar()
        self.intensityVar.set(  80)
        self.blurVar            = IntVar()
        self.blurVar.set(       1)
        self.seed               = IntVar()
        self.seed.set(randint(  0,99999))
        self.invertState        = IntVar()
        self.invertState.set(   0)
        self.colorState         = IntVar()
        self.colorState.set(    0)

        self.activeState        = IntVar()
        self.activeState.set(   1)

    def create_widgets(self, parent):
        self.mainFrame      = parent
        self.cageFrame		= Frame(self.mainFrame)
 
        self.topFrame                               = Frame(         self.cageFrame)

        self.pixelSizeLabel          = Label(         self.topFrame, text='Pixel Size\t(px)')
        self.pixelSizeSpinbox        = Spinbox(       self.topFrame, from_=0, to_=255, textvariable=self.pixelSizeVar, justify='right', width=6)
        self.blurLabel               = Label(         self.topFrame, text='Blur\t(px)')
        self.blurSpinbox             = Spinbox(       self.topFrame, from_=0, to_=9999, textvariable=self.blurVar, justify='right', width=6)
        self.stretchWidthLabel       = Label(         self.topFrame, text='Stretch X\t(%)')
        self.stretchWidthSpinbox     = Spinbox(       self.topFrame, from_=0, to_=100, textvariable=self.stretchWidthVar, command=self.update_widgets_config,   justify='right', width=6)
        self.stretchWidthScale       = Scale(         self.topFrame, from_=0, to_=100, variable=self.stretchWidthVar, orient='horizontal', command=self.update_widgets_config)
        self.stretchHeightLabel      = Label(         self.topFrame, text='Stretch Y\t(%)')
        self.stretchHeightSpinbox    = Spinbox(       self.topFrame, from_=0, to_=100, textvariable=self.stretchHeightVar, command=self.update_widgets_config,  justify='right', width=6)
        self.stretchHeightScale      = Scale(         self.topFrame, from_=0, to_=100, variable=self.stretchHeightVar, orient='horizontal', command=self.update_widgets_config)

        self.contrastLabel           = Label(         self.topFrame, text='Contrast\t(%)')
        self.contrastSpinbox         = Spinbox(       self.topFrame, from_=-50, to_=50, textvariable=self.contrastVar, command=self.update_widgets_config,   justify='right', width=6)
        self.contrastScale           = Scale(         self.topFrame, from_=-50, to_=50, variable=self.contrastVar, orient='horizontal', command=self.update_widgets_config)

        self.firstSeparator          = Separator(     self.topFrame)
        
        self.darkBrightLabel         = Label(         self.topFrame, text='Grain lightnes (Min / Max)')
        self.darkSpinbox             = Spinbox(       self.topFrame, from_=0, to_=255, textvariable=self.darkVar, command=self.update_widgets_config,   justify='right', width=6)
        self.darkScale               = Scale(         self.topFrame, from_=0, to_=255, variable=self.darkVar, orient='horizontal', command=self.update_widgets_config)
        self.brightSpinbox           = Spinbox(       self.topFrame, from_=1, to_=255, textvariable=self.brightVar, command=self.update_widgets_config, justify='right', width=6)
        self.brightScale             = Scale(         self.topFrame, from_=1, to_=255, variable=self.brightVar, orient='horizontal', command=self.update_widgets_config)
        
        self.secondSeparator         = Separator(     self.topFrame)

        self.intensityLabel          = Label(         self.topFrame, text='Visibility\t(%)') # Intensity
        self.intensitySpinbox        = Spinbox(       self.topFrame, from_=0, to_=100, textvariable=self.intensityVar, command=self.update_widgets_config,  justify='right', width=6)
        self.intensityScale          = Scale(         self.topFrame, from_=0, to_=100, variable=self.intensityVar, orient='horizontal', command=self.update_widgets_config)
        
        self.checkbuttonFrame        = Frame(         self.topFrame)
        self.invertCheckbutton       = Checkbutton(   self.checkbuttonFrame, text='Invert', variable=self.invertState)  
        self.colorCheckbutton        = Checkbutton(   self.checkbuttonFrame, text='Colored', variable=self.colorState)  

        self.seedFrame               = Frame(         self.topFrame)
        self.seedLabel               = Label(         self.seedFrame, text='Seed (0 - 99999)')
        self.randomSeedButton        = Button(        self.seedFrame, text=unicodeSymbols[0], command=lambda:self.seed.set(randint(0,99999)))
        self.seedSpinbox             = Spinbox(       self.seedFrame, from_=0, to_=99999, textvariable=self.seed, justify='right', width=6)

        try:
            self.pixelSizeSpinbox.config(       font=self.master.mainWindow.defaultFont)
            self.stretchWidthSpinbox.config(    font=self.master.mainWindow.defaultFont)
            self.stretchHeightSpinbox.config(   font=self.master.mainWindow.defaultFont)
            self.darkSpinbox.config(            font=self.master.mainWindow.defaultFont)
            self.brightSpinbox.config(          font=self.master.mainWindow.defaultFont)
            self.contrastSpinbox.config(        font=self.master.mainWindow.defaultFont)
            self.intensitySpinbox.config(       font=self.master.mainWindow.defaultFont)
            self.blurSpinbox.config(            font=self.master.mainWindow.defaultFont)
            self.seedSpinbox.config(            font=self.master.mainWindow.defaultFont)
        except:
            pass

    def display_widgets(self):
        self.cageFrame.grid(column=0, row=0, sticky='we', padx=3)
        self.cageFrame.columnconfigure(0, weight=1)
        self.cageFrame.columnconfigure(1, weight=0)
        self.cageFrame.rowconfigure(0, weight=0)
        self.cageFrame.rowconfigure(1, weight=0)

        self.topFrame.grid(column=0, row=0, sticky='we')
        self.topFrame.columnconfigure(0, weight=1)
        self.topFrame.columnconfigure(1, weight=0)

        self.pixelSizeLabel.grid(       column=0, row=0, sticky='we', pady=3)
        self.pixelSizeSpinbox.grid(     column=1, row=0, sticky='w')
        self.blurLabel.grid(            column=0, row=1, sticky='we', pady=3)
        self.blurSpinbox.grid(          column=1, row=1, sticky='w')
        self.stretchWidthLabel.grid(    column=0, row=2, sticky='we', pady=3)
        self.stretchWidthSpinbox.grid(  column=1, row=2, sticky='w')
        self.stretchWidthScale.grid(    column=0, row=3, sticky='we', columnspan=2)
        self.stretchHeightLabel.grid(   column=0, row=4, sticky='we', pady=3)
        self.stretchHeightSpinbox.grid( column=1, row=4, sticky='w')
        self.stretchHeightScale.grid(   column=0, row=5, sticky='we', columnspan=2)

        self.contrastLabel.grid(        column=0, row=6, sticky='we', pady=3)
        self.contrastSpinbox.grid(      column=1, row=6, sticky='w')
        self.contrastScale.grid(        column=0, row=7, sticky='we', columnspan=2)

        self.firstSeparator.grid(       column=0, row=8, sticky='we', columnspan=2, pady=10)
        
        self.darkBrightLabel.grid(      column=0, row=9, sticky='we', pady=3, columnspan=2)
        self.darkSpinbox.grid(          column=1, row=10, sticky='w', pady=3)
        self.darkScale.grid(            column=0, row=10, sticky='we')
        self.brightSpinbox.grid(        column=1, row=11, sticky='w', pady=3)
        self.brightScale.grid(          column=0, row=11, sticky='we')

        self.secondSeparator.grid(      column=0, row=12, sticky='we', columnspan=2, pady=10)

        self.intensityLabel.grid(       column=0, row=13, sticky='we', pady=3)
        self.intensitySpinbox.grid(     column=1, row=13, sticky='w')
        self.intensityScale.grid(       column=0, row=14, sticky='we', columnspan=2)

        self.checkbuttonFrame.grid(     column=0, row=15, sticky='we', columnspan=2)
        self.checkbuttonFrame.columnconfigure(0, weight=0)
        self.checkbuttonFrame.columnconfigure(1, weight=0)
        self.invertCheckbutton.grid(    column=0, row=0, sticky='w', pady=6)
        self.colorCheckbutton.grid(     column=1, row=0, sticky='w', pady=6)

        self.seedFrame.grid(            column=0, row=16, sticky='we', columnspan=2)
        self.seedFrame.columnconfigure(0, weight=0)
        self.seedFrame.columnconfigure(1, weight=0)
        self.seedFrame.columnconfigure(3, weight=0)
        self.seedLabel.grid(            column=0, row=0, sticky='we', pady=3)
        self.randomSeedButton.grid(     column=1, row=0, sticky='w')
        self.seedSpinbox.grid(          column=2, row=0, sticky='e')

    def random_values(self):
        if self.activeState.get():
            #Function gets executed, when 'Random Render' Button is hit
            pass

    def update_widgets_config(self, event=None):
        if self.activeState.get():
            self.darkVar.set(   '%0.0f' % float(self.darkVar.get()))
            self.brightVar.set( '%0.0f' % float(self.brightVar.get()))
            if self.darkVar.get() >= self.brightVar.get():
                self.darkVar.set(self.brightVar.get()-1)

            self.stretchWidthVar.set(   '%0.0f' % float(self.stretchWidthVar.get()))
            self.stretchHeightVar.set(  '%0.0f' % float(self.stretchHeightVar.get()))
            self.contrastVar.set(       '%0.0f' % float(self.contrastVar.get()))
            self.intensityVar.set(      '%0.0f' % float(self.intensityVar.get()))

    def applyFilter(self, image):
        if self.activeState.get():
            print('Burning Noise Filter: started')
            self.update_widgets_config()
            seed(self.seed.get())
            np.random.seed(self.seed.get())
            sourceImage = copy(image)
            sourceImage.load()
            width, height = sourceImage.size
            size = width, height

            noiseHeight = int((height / self.pixelSizeVar.get()) - (height / self.pixelSizeVar.get()) / 100 * self.stretchHeightVar.get())
            noiseWidth  = int((width  / self.pixelSizeVar.get()) - (width  / self.pixelSizeVar.get()) / 100 * self.stretchWidthVar.get())

            if self.colorState.get():
                noiseDataOne    = np.random.randint(self.darkVar.get(), self.brightVar.get(), (noiseHeight*noiseWidth))
                noiseDataTwo    = np.random.randint(self.darkVar.get(), self.brightVar.get(), (noiseHeight*noiseWidth))
                noiseDataThree  = np.random.randint(self.darkVar.get(), self.brightVar.get(), (noiseHeight*noiseWidth))
                noiseData       = list(zip(noiseDataOne, noiseDataTwo, noiseDataThree))

                tempNoiseMask   = Image.new('RGB', (noiseWidth, noiseHeight))
                noiseMask       = Image.new('RGB', size)
                tempNoiseMask.putdata(noiseData)

                noiseMask = tempNoiseMask.resize(size, resample=Image.NEAREST)
            else:
                noiseData       = np.random.randint(self.darkVar.get(), self.brightVar.get(), (noiseHeight*noiseWidth))

                tempNoiseMask   = Image.new('L', (noiseWidth, noiseHeight))
                noiseMask       = Image.new('L', size)
                tempNoiseMask.putdata(noiseData)

                noiseMask = tempNoiseMask.resize(size, resample=Image.NEAREST)
                noiseMask = noiseMask.convert('RGB')

            burnedImage = copy(sourceImage)
            tempContrast = float(1-(self.contrastVar.get()+50)/100)

            if tempContrast <= 0.0: 
                tempContrast = 0.001

            if self.invertState.get():
                burnedImage = ImageChops.subtract(noiseMask, burnedImage, tempContrast)
            else:
                burnedImage = ImageChops.subtract(burnedImage, noiseMask, tempContrast)

            if self.blurVar.get() != 0:
                burnedImage = burnedImage.filter(ImageFilter.GaussianBlur(self.blurVar.get()))

            tempAlpha = float(self.intensityVar.get() / 100)

            image = ImageChops.blend(sourceImage, burnedImage, tempAlpha)

            seed()
            np.random.seed()
            del self.randomNoiseData[:]
            print('Burning Noise Filter: finished')
        return image