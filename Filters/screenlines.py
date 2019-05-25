import numpy as np
from PIL import Image, ImageChops, ImageFilter, ImageDraw
from tkinter import IntVar, StringVar, colorchooser, Canvas
from tkinter.ttk import Frame, Label, Button, Entry, Checkbutton, Separator, Spinbox, Scale, OptionMenu
from copy import copy
from random import randint, uniform
from blend_modes import soft_light, lighten_only, addition, darken_only, subtract, grain_merge, divide

class ScreenLinesFilter():
    def __init__(self, parent, master):
        self.parent = parent
        self.master = master

        self.name = 'Screen Lines'

        self.create_parameters()
        self.create_widgets(parent)
        #self.mainFrame.columnconfigure(0, weight=0)
        #self.mainFrame.columnconfigure(1, weight=0)
        #self.mainFrame.columnconfigure(2, weight=0)
        #self.mainFrame.rowconfigure(0, weight=0)
        #self.mainFrame.rowconfigure(1, weight=0, pad=20)
        #self.mainFrame.rowconfigure(2, weight=1)

    def create_parameters(self):
        self.lineDensity    = IntVar()
        self.lineDensity.set(42)
        self.lineThickness  = IntVar()
        self.lineThickness.set(5)
        self.lineBlur       = IntVar()
        self.lineBlur.set(1)
        self.blendmodeList  = ['Soft Light', 'Lighten Only', 'Darken Only', 'Addition', 'Subtract', 'Divide', 'Grain Merge']
        self.blendmode      = StringVar()
        self.blendmode.set(self.blendmodeList[0])

        self.randomVar      = IntVar()
        self.randomVar.set(0)
        self.invertVar      = IntVar()
        self.invertVar.set(0)

        self.lineColor = (255, 255, 255)

        self.activeState = IntVar()
        self.activeState.set(1)

    def create_widgets(self, parent):
        self.mainFrame      = parent
        self.cageFrame		= Frame(self.mainFrame) # Parent of all widgets

        self.topFrame               = Frame(        self.cageFrame)

        self.lineDensityLabel       = Label(        self.topFrame, text='Density\t(%)')
        self.lineDensitySpinbox     = Spinbox(      self.topFrame, from_=1, to_=99,     textvariable=   self.lineDensity,   justify='right',  width=6)
        self.lineDensityScale       = Scale(        self.topFrame, from_=1, to_=99,     variable=       self.lineDensity,   orient='horizontal', command=lambda s:self.lineDensity.set('%0.0f' % float(s)))
        self.lineThicknessLabel     = Label(        self.topFrame, text='Thickness\t(px)')
        self.lineThicknessSpinbox   = Spinbox(      self.topFrame, from_=0, to_=9999,   textvariable=self.lineThickness,    justify='right', width=6)
        self.lineBlurLabel          = Label(        self.topFrame, text='Blur\t(px)')
        self.lineBlurSpinbox        = Spinbox(      self.topFrame, from_=0, to_=9999,   textvariable=self.lineBlur,         justify='right', width=6)

        self.blendmodeFrame         = Frame(        self.cageFrame)
        self.blendmodeLabel         = Label(        self.blendmodeFrame, text='Blend Mode:')
        self.blendmodeOptionmenu    = OptionMenu(   self.blendmodeFrame, self.blendmode, self.blendmodeList[0], *self.blendmodeList)
        
        try:
            self.lineDensitySpinbox.config(         font=self.master.mainWindow.defaultFont)
            self.lineThicknessSpinbox.config(       font=self.master.mainWindow.defaultFont)
            self.lineBlurSpinbox.config(            font=self.master.mainWindow.defaultFont)
            self.blendmodeOptionmenu['menu'].config(font=self.master.mainWindow.defaultFont)
            #self.blendmodeOptionmenu['menu'].config(bg=self.master.mainWindow.backgroundColor, fg=self.master.mainWindow.fontColor)
        except:
            pass

        self.checkbuttonFrame       = Frame(        self.cageFrame)
        self.randomCheckbutton      = Checkbutton(  self.checkbuttonFrame, text='Random', variable=self.randomVar)

        self.colorChoserFrame       = Frame(        self.cageFrame)
        self.colorChoserLabel       = Label(        self.colorChoserFrame, text='Line Color:')
        self.colorCanvas            = Canvas(       self.colorChoserFrame, height=25, background='#%02x%02x%02x' % self.lineColor, cursor='hand2', highlightbackground='gray30', highlightthickness=3)
        self.colorCanvas.bind('<Button-1>', self.change_line_color)

    def change_line_color(self, event=None):
        tempColor = colorchooser.askcolor(color=self.lineColor, title='Line Color')

        if tempColor != (None, None):
            self.lineColor = (int(tempColor[0][0]), int(tempColor[0][1]), int(tempColor[0][2]))
            hexColor = '#%02X%02X%02X' % self.lineColor
            self.colorCanvas.config(background=hexColor)

    def display_widgets(self):
        self.mainFrame.columnconfigure( 0, weight=1)
        self.mainFrame.rowconfigure(    0, weight=1)

        self.cageFrame.grid(column=0, row=0, sticky='we', padx=3)
        self.cageFrame.columnconfigure(0, weight=1)
        self.cageFrame.rowconfigure(0, weight=0)
        self.cageFrame.rowconfigure(1, weight=0, pad=15)
        self.cageFrame.rowconfigure(2, weight=1)
        
        self.topFrame.grid(             column=0, row=0, sticky='we')
        self.topFrame.columnconfigure(0, weight=1)
        self.topFrame.rowconfigure(0, weight=0)
        self.topFrame.rowconfigure(1, weight=0)
        self.topFrame.rowconfigure(2, weight=0)
        self.topFrame.rowconfigure(3, weight=1)

        self.lineDensityLabel.grid(     column=0, row=0, sticky='we', pady=3)
        self.lineDensitySpinbox.grid(   column=1, row=0, sticky='w')
        self.lineDensityScale.grid(     column=0, row=1, sticky='we', columnspan=2)
        self.lineThicknessLabel.grid(   column=0, row=2, sticky='we', pady=3)
        self.lineThicknessSpinbox.grid( column=1, row=2, sticky='w')
        self.lineBlurLabel.grid(        column=0, row=3, sticky='we', pady=3)
        self.lineBlurSpinbox.grid(      column=1, row=3, sticky='w')

        self.blendmodeFrame.grid(       column=0, row=4, sticky='w', columnspan=2)
        self.blendmodeLabel.grid(       column=0, row=0, sticky='w', pady=6)
        self.blendmodeOptionmenu.grid(  column=1, row=0, sticky='w')

        self.checkbuttonFrame.grid(     column=0, row=5, sticky='we')
        self.checkbuttonFrame.columnconfigure(0, weight=1)
        self.randomCheckbutton.grid(    column=0, row=0, sticky='w', pady=5)

        self.colorChoserFrame.grid(     column=0, row=6, sticky='we')
        self.colorChoserFrame.columnconfigure(0, weight=1)
        self.colorChoserLabel.grid(     column=0, row=0, sticky='we', pady=3)
        self.colorCanvas.grid(          column=0, row=1, sticky='we')

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
            print(self.name, ': started')
            #Create Variables
            sourceImage = copy(image)
            #sourceData   = sourceImage.getdata()
            width, height = sourceImage.size
            size        = width, height

            maskImage       = Image.new('RGB', size, color=(0,0,0))
            draw            = ImageDraw.Draw(maskImage, 'RGB')

            try:    #Catch division by zero
                lineSpacing     = int(100 / self.lineDensity.get())
            except:
                lineSpacing     = int(100 / 1)

            try:    #Catch division by zero
                lineCount       = int((height / (self.lineThickness.get() + lineSpacing))) +2
            except:
                lineCount       = int((height / 1)) +2

            lineColor       = self.lineColor
            lineColorScale  = 1.0

            for x in range(lineCount):
                if self.randomVar.get():
                    lineColorScale  = uniform(0.7, 1.0)
                    lineColor       = (int(self.lineColor[0] * lineColorScale), int(self.lineColor[1] * lineColorScale), int(self.lineColor[2] * lineColorScale))
                draw.line(((0,x*(lineSpacing+self.lineThickness.get())), (width,x*(lineSpacing+self.lineThickness.get()))), fill=lineColor, width=self.lineThickness.get())

            del draw
            maskImage   = maskImage.filter(ImageFilter.GaussianBlur(self.lineBlur.get()))
            maskImage   = maskImage.convert('RGBA')
            sourceImage = sourceImage.convert('RGBA')

            #try:
            maskImage   = np.array(maskImage)   #Convert Pillow Image to numpy array,
            sourceImage = np.array(sourceImage)    # for usage in blend_modes module
            maskImage   = maskImage.astype(float)
            sourceImage = sourceImage.astype(float)

            if self.blendmode.get() == 'Soft Light':
                sourceImage = soft_light(sourceImage, maskImage, 1.0)

            elif self.blendmode.get() == 'Lighten Only':
                sourceImage = lighten_only(sourceImage, maskImage, 1.0)

            elif self.blendmode.get() == 'Addition':
                sourceImage = addition(sourceImage, maskImage, 1.0)

            elif self.blendmode.get() == 'Darken Only':
                sourceImage = darken_only(sourceImage, maskImage, 1.0)

            elif self.blendmode.get() == 'Subtract':
                sourceImage = subtract(sourceImage, maskImage, 1.0)

            elif self.blendmode.get() == 'Grain Merge':
                sourceImage = grain_merge(sourceImage, maskImage, 1.0)

            elif self.blendmode.get() == 'Divide':
                sourceImage = divide(sourceImage, maskImage, 1.0)
            #except MemoryError:
            #    glitchLogger.exception('Memory Error with ScreenFilter!')
            #    showerror('Memory Error', 'Ran out of Memory!\n\nSolutions:\n - Use 64bit Python\n - Use smaller Images\n - Deactivate "Screen Lines"')

            image = np.uint8(sourceImage)
            image = Image.fromarray(image)
            image = image.convert('RGB')

            print(self.name, ': finished')

        return image