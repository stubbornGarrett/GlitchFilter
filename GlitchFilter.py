#Python 3.7
from PIL import Image, ImageChops, ImageTk, ImageColor, ImageDraw, ImageFilter, ImageStat
from tkinter import filedialog, ttk
from tkinter.messagebox import askyesno, showinfo, showwarning, showerror
from logging.handlers import RotatingFileHandler
import logging
import tkinter as tk
import numpy as np
import blend_modes
import random
import os
import copy
import math
import time
import datetime
import threading

#Logger
glitchLogger = logging.getLogger(__name__)
glitchLogger.setLevel(logging.DEBUG)

glitchFileHandler = RotatingFileHandler('GlitchFilterLog.log', maxBytes=100000)
glitchFileHandler.setLevel(logging.INFO)

glitchLogger.addHandler(glitchFileHandler)

glitchLogger.info('******************** {} - Session ********************'.format(datetime.datetime.now()))

glitchFormatter = logging.Formatter('%(asctime)s) - %(levelname)s: %(message)s')
glitchFileHandler.setFormatter(glitchFormatter)

#global settings
HEIGHT      = 800
WIDTH       = 1200
imagWidth   = 770
confWidth   = WIDTH - HEIGHT
bgColor     = '#303030'
secColor    = '#505050'
thiColor    = 'gray30'
fouColor    = '#007777'
textColor   = '#ffffff'
unicodeSymbols = [u'\u21bb'] #0=ClockwiseCircleArrow

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()

        self.sourceImagePath        = ''                                #Filepath to chosen Image
        self.sourceImageExtension  = ".png"                             #Extension of chosen Image
        self.sourceImage = Image.new('L', (1,1), color='pink')          #PIL Image of the chosen Image
        self.tempImage = self.sourceImage                               #PIL Image of the altered  Image
        self.thumbImage = tk.PhotoImage(self.tempImage.load())          #TkPhoto Image as a thumbnail

        self.FILEOPTIONS =  dict(   filetypes=[\
                                    ('JPEG','*.jpg *.jpeg'), 
                                    ('PNG','*.png'),
                                    ("all files","*.*")])

        #Main Window parameters
        self.master.resizable(False, False)
        self.master.geometry('+50+50')
        self.master.title('Glitch Filter')
        self.master.protocol('WM_DELETE_WINDOW', self.quit_program)
        self.master.tk_setPalette(
            background=bgColor, 
            foreground=textColor, 
            activeForeground='gray60', 
            activeBackground=fouColor)
        try:
            self.master.iconbitmap('GlitchFilterIcon.ico')
        except:
            glitchLogger.warning("Icon couldn't be loaded - main window")

        #Main Variables
        self.filterQueue        = [self.rgbOffsetFilter, self.bigBlocksFilter, self.smallBlocksFilter, self.burnNoiseFilter, self.rgbScreenFilter, self.screenLinesFilter, self.testFilter]
        self.filterList         = ['RGB Offset', 'Big Blocks', 'Small Blocks', 'Burning Noise', 'RGB Screen', 'Screen Lines']
        self.filterListVar      = tk.StringVar()
        self.filterListVar.set(self.filterList)

        self.previewActiveVar   = tk.IntVar()   #Keeps track if the Image preview is active
        self.previewActiveVar.set(1)            #Default -> active

        self.setupFinished      = False
        self.firstImageLoaded   = False
        self.isImageSaved       = True          #Keeps track if any changes were made

        self.maxThreads = 400   #At this point not important (was used for experimental multithreading with unknown amount of threads)

        #Open Window Variables - keeps track if toplevel windows are open
        self.imagePreviewOpen   = False
        self.filterListOpen     = False
        self.presetListOpen     = False
        self.aboutWindowOpen    = False

        #Create parameters for the Filters and insert default Values
        try:
            self.create_parameters()
            glitchLogger.info('Initial creation of parameters successful...')
        except:
            glitchLogger.exception('Initial creation of parameters failed!')
            showerror('Fatal Error', 'Initial creation of parameters failed!')
            raise

        #Create all Widgets
        try:
            self.create_widgets()
            glitchLogger.info('Initial creation of widgets successful...')
        except:
            glitchLogger.exception('Initial creation of widgets failed!')
            showerror('Fatal Error', 'Initial creation of widgets failed!')
            raise

        #Checks for activated Filters
        try:
            self.refresh_filter()
            glitchLogger.info('Initial refresh of filter successful...')
        except:
            glitchLogger.exception('Initial refresh of filter failed!')
            showerror('Fatal Error', 'Initial refresh of filter failed!')
            raise

        self.setupFinished = True

        #Updates colored Labels
        self.update_labels()

        glitchLogger.info('Initialisation succeeded...')


    def create_parameters(self):
        #RGBoffsetFilter parameters
        self.rgbOffsetFilterRedXvar = tk.IntVar()
        self.rgbOffsetFilterRedXvar.set(5)
        self.rgbOffsetFilterRedYvar = tk.IntVar()
        self.rgbOffsetFilterRedYvar.set(5)
        self.rgbOffsetFilterGreenXvar = tk.IntVar()
        self.rgbOffsetFilterGreenXvar.set(-5)
        self.rgbOffsetFilterGreenYvar = tk.IntVar()
        self.rgbOffsetFilterGreenYvar.set(5)
        self.rgbOffsetFilterBlueXvar = tk.IntVar()
        self.rgbOffsetFilterBlueXvar.set(5)
        self.rgbOffsetFilterBlueYvar = tk.IntVar()
        self.rgbOffsetFilterBlueYvar.set(-5)
        
        self.rgbOffsetFilterBetterCheckButtonState = tk.IntVar()
        self.rgbOffsetFilterBetterCheckButtonState.set(1)
        self.rgbOffsetFilterActiveState = tk.IntVar()
        self.rgbOffsetFilterActiveState.set(1)

        #BigBlocksOffsetFilter parameters
        self.bigBlocksFilterBlockCountVar = tk.IntVar()
        self.bigBlocksFilterBlockCountVar.set(5)
        self.bigBlocksFilterBlockMaxHeight = tk.IntVar()
        self.bigBlocksFilterBlockMaxHeight.set(1)
        self.bigBlocksFilterBlockMaxOffset = tk.IntVar()
        self.bigBlocksFilterBlockMaxOffset.set(10)

        self.bigBlocksFilterSeedVar = tk.IntVar()
        self.bigBlocksFilterSeedVar.set(int(random.randint(0, 99999)))

        self.bigBlocksFilterActiveState = tk.IntVar()
        self.bigBlocksFilterActiveState.set(1)

        #Small Blocks Filter
        self.smallBlocksFilterBlocksCount = tk.IntVar()
        self.smallBlocksFilterBlocksCount.set(300)
        self.smallBlocksFilterMinWidth = tk.IntVar()
        self.smallBlocksFilterMinWidth.set(100)
        self.smallBlocksFilterMaxWidth = tk.IntVar()
        self.smallBlocksFilterMaxWidth.set(150)
        self.smallBlocksFilterMinHeight = tk.IntVar()
        self.smallBlocksFilterMinHeight.set(1)
        self.smallBlocksFilterMaxHeight = tk.IntVar()
        self.smallBlocksFilterMaxHeight.set(10)
        
        self.smallBlocksFilterSeed = tk.IntVar()
        self.smallBlocksFilterSeed.set(random.randint(0,99999))

        self.smallBlocksFilterActiveState = tk.IntVar()
        self.smallBlocksFilterActiveState.set(1)

        #Screen Lines parameters
        self.screenLinesFilterLineDensity = tk.IntVar()
        self.screenLinesFilterLineDensity.set(42)
        self.screenLinesFilterLineThickness = tk.IntVar()
        self.screenLinesFilterLineThickness.set(5)
        self.screenLinesFilterLineBlur = tk.IntVar()
        self.screenLinesFilterLineBlur.set(1)
        self.screenLinesFilterBlendmodeList = ['Soft Light', 'Lighten Only', 'Darken Only', 'Addition', 'Subtract', 'Divide', 'Grain Merge']
        self.screenLinesFilterBlendmode = tk.StringVar()
        self.screenLinesFilterBlendmode.set(self.screenLinesFilterBlendmodeList[0])

        self.screenLinesFilterRandomVar = tk.IntVar()
        self.screenLinesFilterRandomVar.set(0)
        self.screenLinesFilterInvert = tk.IntVar()
        self.screenLinesFilterInvert.set(0)

        self.screenLinesFilterLineColorRed = tk.IntVar()
        self.screenLinesFilterLineColorRed.set(255)
        self.screenLinesFilterLineColorRed.trace('w', self.update_labels)
        self.screenLinesFilterLineColorGreen = tk.IntVar()
        self.screenLinesFilterLineColorGreen.set(255)
        self.screenLinesFilterLineColorGreen.trace('w', self.update_labels)
        self.screenLinesFilterLineColorBlue = tk.IntVar()
        self.screenLinesFilterLineColorBlue.set(255)
        self.screenLinesFilterLineColorBlue.trace('w', self.update_labels)

        self.screenLinesFilterActiveState = tk.IntVar()
        self.screenLinesFilterActiveState.set(1)

        #Burning Noise Filter parameters
        self.lock = threading.Lock()
        self.randomNoiseData = []

        self.burnNoiseFilterPixelSize = tk.IntVar()
        self.burnNoiseFilterPixelSize.set(2)
        self.burnNoiseFilterStretchWidth = tk.IntVar()
        self.burnNoiseFilterStretchWidth.set(60)
        self.burnNoiseFilterStretchHeight = tk.IntVar()
        self.burnNoiseFilterStretchHeight.set(0)
        self.burnNoiseFilterBright = tk.IntVar()
        self.burnNoiseFilterBright.set(150)
        self.burnNoiseFilterDark = tk.IntVar()
        self.burnNoiseFilterDark.set(20)
        self.burnNoiseFilterContrast = tk.IntVar()
        self.burnNoiseFilterContrast.set(40)
        self.burnNoiseFilterIntensity = tk.IntVar()
        self.burnNoiseFilterIntensity.set(80)
        self.burnNoiseFilterBlur = tk.IntVar()
        self.burnNoiseFilterBlur.set(1)
        self.burnNoiseFilterSeed = tk.IntVar()
        self.burnNoiseFilterSeed.set(random.randint(0,99999))
        self.burnNoiseFilterInvert = tk.IntVar()
        self.burnNoiseFilterInvert.set(0)
        self.burnNoiseFilterColor = tk.IntVar()
        self.burnNoiseFilterColor.set(0)

        self.burnNoiseFilterActiveState = tk.IntVar()
        self.burnNoiseFilterActiveState.set(1)

        #RBG Screen
        self.rgbScreenFilterPixelSize = tk.IntVar()
        self.rgbScreenFilterPixelSize.set(3)
        self.rgbScreenFilterPixelGap = tk.IntVar()
        self.rgbScreenFilterPixelGap.set(1)
        self.rgbScreenFilterIntensity = tk.IntVar()
        self.rgbScreenFilterIntensity.set(80)
        self.rgbScreenFilterBlur = tk.IntVar()
        self.rgbScreenFilterBlur.set(0)

        self.rgbScreenFilterFirstRed = tk.IntVar()
        self.rgbScreenFilterFirstRed.set(0)
        self.rgbScreenFilterFirstRed.trace('w', self.update_labels)
        self.rgbScreenFilterFirstGreen = tk.IntVar()
        self.rgbScreenFilterFirstGreen.set(255)
        self.rgbScreenFilterFirstGreen.trace('w', self.update_labels)
        self.rgbScreenFilterFirstBlue = tk.IntVar()
        self.rgbScreenFilterFirstBlue.set(255)
        self.rgbScreenFilterFirstBlue.trace('w', self.update_labels)

        self.rgbScreenFilterSecondRed = tk.IntVar()
        self.rgbScreenFilterSecondRed.set(255)
        self.rgbScreenFilterSecondRed.trace('w', self.update_labels)
        self.rgbScreenFilterSecondGreen = tk.IntVar()
        self.rgbScreenFilterSecondGreen.set(0)
        self.rgbScreenFilterSecondGreen.trace('w', self.update_labels)
        self.rgbScreenFilterSecondBlue = tk.IntVar()
        self.rgbScreenFilterSecondBlue.set(255)
        self.rgbScreenFilterSecondBlue.trace('w', self.update_labels)

        self.rgbScreenFilterThirdRed = tk.IntVar()
        self.rgbScreenFilterThirdRed.set(255)
        self.rgbScreenFilterThirdRed.trace('w', self.update_labels)
        self.rgbScreenFilterThirdGreen = tk.IntVar()
        self.rgbScreenFilterThirdGreen.set(255)
        self.rgbScreenFilterThirdGreen.trace('w', self.update_labels)
        self.rgbScreenFilterThirdBlue = tk.IntVar()
        self.rgbScreenFilterThirdBlue.set(0)
        self.rgbScreenFilterThirdBlue.trace('w', self.update_labels)

        self.rgbScreenFilterActiveState = tk.IntVar()
        self.rgbScreenFilterActiveState.set(0)

        #List of all Variables
        self.variableList = [self.rgbOffsetFilterRedXvar, self.rgbOffsetFilterRedYvar, self.rgbOffsetFilterGreenXvar, self.rgbOffsetFilterGreenYvar, self.rgbOffsetFilterBlueXvar, self.rgbOffsetFilterBlueYvar]

    def create_widgets(self):
        #Menubar**********************************************************************************************
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)

        self.fileMenu = tk.Menu(self.menubar, tearoff=0)
        self.helpMenu = tk.Menu(self.menubar, tearoff=0)

        #File
        self.menubar.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='Open Image', accelerator='Ctrl+O', command=self.browse_file)
        self.fileMenu.add_command(label='Save', accelerator='Ctrl+S', command=self.save_image)
        self.fileMenu.add_command(label='Save Image as...', accelerator='Ctrl+Alt+S', command=self.save_image_as)
        self.fileMenu.add_command(label='Exit', command=self.quit_program)
        
        self.bind_all('<Control-o>', self.browse_file)
        self.bind_all('<Control-s>', self.save_image)
        self.bind_all('<Control-Alt-s>', self.save_image_as)

        #Help
        self.menubar.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='About', command=self.open_about_window)

        #define widgets****************************************************************************************
        self.imageFrame         = tk.Frame(         self, width=imagWidth, height=HEIGHT, padx=3, pady=3)   #Big Left Parent
        self.imageLabelFrame    = tk.LabelFrame(    self.imageFrame, text='Image Preview')
        self.imageCanvas        = tk.Canvas(        self.imageLabelFrame, bg='gray42', height=750, width=750)
        self.imageProgressbar   = ttk.Progressbar(  self.imageFrame, length=750, orient=tk.HORIZONTAL, mode='indeterminate')
        
        self.configFrame        = tk.Frame(         self, width=confWidth, height=HEIGHT, padx=2, pady=2)   #Big Right Parent
        self.topConfigFrame     = tk.Frame(         self.configFrame, width=confWidth)
        self.configFilterFrame  = tk.Frame(         self.configFrame, width=confWidth-12,  height=550, relief=tk.GROOVE, bd=2)
        self.bottomConfigFrame  = tk.Frame(         self.configFrame, width=confWidth, height=300)
        
        #Overview Top
        self.filterListScrollbar                    = tk.Scrollbar(     self.topConfigFrame, orient=tk.VERTICAL)
        self.filterListListbox                      = tk.Listbox(       self.topConfigFrame, selectmode=tk.SINGLE, listvariable=self.filterListVar, height=4, xscrollcommand=self.filterListScrollbar.set, exportselection=0, selectbackground='white', selectforeground='black')
        self.filterListListbox.bind('<<ListboxSelect>>', self.switch_filter_options)

        self.filterListButton                       = tk.Button(        self.topConfigFrame, text='Active Filter List', command=self.open_filterList_window, height=1, width=15)
        self.presetListButton                       = tk.Button(        self.topConfigFrame, text='Presets', state='disable', command=self.open_presetList_window, height=1, width=15)#, font=('Helvetica', '16'))
        self.presetListButtonTooltip                = CreateToolTip(    self.presetListButton, 'Not implemented yet')

        #Overview Bottom
        self.previewButton                          = tk.Button(        self.bottomConfigFrame, text='Preview full sized Image', command=self.preview_fullsized_image, width=28)
        self.randomButton                           = tk.Button(        self.bottomConfigFrame, text='Random Render ', command=self.rand_values)
        self.renderButton                           = tk.Button(        self.bottomConfigFrame, text='Apply Changes', command=self.apply_changes)
        self.previewActiveCheckbutton               = tk.Checkbutton(   self.bottomConfigFrame, text='Preview', selectcolor='gray30', variable=self.previewActiveVar, command=self.update_preview)
        
        #RGBoffsetFilter
        self.rgbOffsetFilterCanvas                  = tk.Canvas(        self.configFilterFrame, width=(confWidth-23), height=500, bd=0, highlightthickness=0)

        self.rgbOffsetFilterRedXlabel               = tk.Label(         self.rgbOffsetFilterCanvas, text='Red X', anchor=tk.W, relief=tk.GROOVE, bg='#440000')
        self.rgbOffsetFilterRedXscale               = tk.Spinbox(       self.rgbOffsetFilterCanvas, from_=-1920, to_=1920, justify=tk.RIGHT, textvariable=self.rgbOffsetFilterRedXvar)#, selectbackground=fouColor)
        self.rgbOffsetFilterGreenXlabel             = tk.Label(         self.rgbOffsetFilterCanvas, text='Green X', anchor=tk.W, relief=tk.GROOVE, bg='#004400')
        self.rgbOffsetFilterGreenXscale             = tk.Spinbox(       self.rgbOffsetFilterCanvas, from_=-1920, to_=1920, justify=tk.RIGHT, textvariable=self.rgbOffsetFilterGreenXvar, selectbackground=fouColor)
        self.rgbOffsetFilterBlueXlabel              = tk.Label(         self.rgbOffsetFilterCanvas, text='Blue X', anchor=tk.W, relief=tk.GROOVE, bg='#000044')
        self.rgbOffsetFilterBlueXscale              = tk.Spinbox(       self.rgbOffsetFilterCanvas, from_=-1920, to_=1920, justify=tk.RIGHT, textvariable=self.rgbOffsetFilterBlueXvar, selectbackground=fouColor)
        self.rgbOffsetFilterRedYlabel               = tk.Label(         self.rgbOffsetFilterCanvas, text='Red Y', anchor=tk.W, relief=tk.GROOVE, bg='#440000')
        self.rgbOffsetFilterRedYscale               = tk.Spinbox(       self.rgbOffsetFilterCanvas, from_=-1080, to_=1080, justify=tk.RIGHT, textvariable=self.rgbOffsetFilterRedYvar, selectbackground=fouColor)
        self.rgbOffsetFilterGreenYlabel             = tk.Label(         self.rgbOffsetFilterCanvas, text='Green Y', anchor=tk.W, relief=tk.GROOVE, bg='#004400')
        self.rgbOffsetFilterGreenYscale             = tk.Spinbox(       self.rgbOffsetFilterCanvas, from_=-1080, to_=1080, justify=tk.RIGHT, textvariable=self.rgbOffsetFilterGreenYvar, selectbackground=fouColor)
        self.rgbOffsetFilterBlueYlabel              = tk.Label(         self.rgbOffsetFilterCanvas, text='Blue Y', anchor=tk.W, relief=tk.GROOVE, bg='#000044')
        self.rgbOffsetFilterBlueYscale              = tk.Spinbox(       self.rgbOffsetFilterCanvas, from_=-1080, to_=1080, justify=tk.RIGHT, textvariable=self.rgbOffsetFilterBlueYvar, selectbackground=fouColor)
       
        self.rgbOffsetFilterBottomFrame             = tk.Frame(         self.rgbOffsetFilterCanvas)
        self.rgbOffsetFilterBetterCheckButton       = tk.Checkbutton(   self.rgbOffsetFilterBottomFrame, text='Nicer Values', selectcolor='gray30', variable=self.rgbOffsetFilterBetterCheckButtonState)
        self.rgbOffsetFilterRandomButton            = tk.Button(        self.rgbOffsetFilterBottomFrame, text='Random Values', command=self.rgbOffset_rand_values)

        #Big Blocks Offset
        self.bigBlocksFilterFrame                   = tk.Frame(         self.configFilterFrame, width=(confWidth-23), height=400, highlightthickness=0)

        self.bigBlocksFilterBlockCountLabel         = tk.Label(         self.bigBlocksFilterFrame, text='Block Count', anchor=tk.W, relief=tk.GROOVE)
        self.bigBlocksFilterBlockCountSpinbox       = tk.Spinbox(       self.bigBlocksFilterFrame, from_=0, to_=20, textvariable=self.bigBlocksFilterBlockCountVar, justify=tk.RIGHT, selectbackground=fouColor, command=self.update_parameters)
        self.bigBlocksFilterBlockMaxHeightLabel     = tk.Label(         self.bigBlocksFilterFrame, text='Max Block Height (px)', anchor=tk.W, relief=tk.GROOVE)
        self.bigBlocksFilterBlockMaxHeightSpinbox   = tk.Spinbox(       self.bigBlocksFilterFrame, from_=0, to_=1, textvariable=self.bigBlocksFilterBlockMaxHeight, justify=tk.RIGHT, selectbackground=fouColor, command=self.update_parameters)
        self.bigBlocksFilterBlockMaxOffsetLabel     = tk.Label(         self.bigBlocksFilterFrame, text='Max Offset (%)', anchor=tk.W, relief=tk.GROOVE)
        self.bigBlocksFilterBlockMaxOffsetSpinbox   = tk.Spinbox(       self.bigBlocksFilterFrame, from_=0, to_=100, textvariable=self.bigBlocksFilterBlockMaxOffset, justify=tk.RIGHT, selectbackground=fouColor)
        self.bigBlocksFilterBlockMaxOffsetScale     = tk.Scale(         self.bigBlocksFilterFrame, from_=0, to_=100, variable=self.bigBlocksFilterBlockMaxOffset, orient=tk.HORIZONTAL, showvalue=0)
        self.bigBlocksFilterSeedLabel               = tk.Label(         self.bigBlocksFilterFrame, text='Seed (0 - 99999)', anchor=tk.W, relief=tk.GROOVE)
        self.bigBlocksFilterSeedSpinbox             = tk.Spinbox(       self.bigBlocksFilterFrame, from_=0, to_=99999, textvariable=self.bigBlocksFilterSeedVar, justify=tk.RIGHT, selectbackground=fouColor)
        self.bigBlocksFilterRandomSeedButton        = tk.Button(        self.bigBlocksFilterFrame, text=unicodeSymbols[0], font=('Arial', '13', 'bold'), height=1, width=3, command=lambda:self.bigBlocksFilterSeedVar.set(random.randint(0,99999)))
        self.rgbOffsetFilterRedXtooltip             = CreateToolTip(    self.bigBlocksFilterRandomSeedButton, 'Generate random Seed between 0 and 99999')

        #Small Blocks Filter
        self.smallBlocksFilterFrame                 = tk.Frame(         self.configFilterFrame, width=(confWidth-23), height=400, highlightthickness=0)

        self.smallBlocksFilterBlockCountLabel       = tk.Label(         self.smallBlocksFilterFrame, text='Block Count', anchor=tk.W, relief=tk.GROOVE)
        self.smallBlocksFilterBlockCountSpinbox     = tk.Spinbox(       self.smallBlocksFilterFrame, from_=0, to_=10000, textvariable=self.smallBlocksFilterBlocksCount, justify=tk.RIGHT, selectbackground=fouColor, command=self.update_parameters)
        self.smallBlocksFilterMinWidthLabel         = tk.Label(         self.smallBlocksFilterFrame, text='Min Width', anchor=tk.W, relief=tk.GROOVE)
        self.smallBlocksFilterMinWidthSpinbox       = tk.Spinbox(       self.smallBlocksFilterFrame, from_=1, to_=200, textvariable=self.smallBlocksFilterMinWidth, justify=tk.RIGHT, selectbackground=fouColor, command=self.update_parameters)
        self.smallBlocksFilterMaxWidthLabel         = tk.Label(         self.smallBlocksFilterFrame, text='Max Width', anchor=tk.W, relief=tk.GROOVE)
        self.smallBlocksFilterMaxWidthSpinbox       = tk.Spinbox(       self.smallBlocksFilterFrame, from_=2, to_=200, textvariable=self.smallBlocksFilterMaxWidth, justify=tk.RIGHT, selectbackground=fouColor, command=self.update_parameters)
        self.smallBlocksFilterMinHeightLabel        = tk.Label(         self.smallBlocksFilterFrame, text='Min Height', anchor=tk.W, relief=tk.GROOVE)
        self.smallBlocksFilterMinHeightSpinbox      = tk.Spinbox(       self.smallBlocksFilterFrame, from_=1, to_=200, textvariable=self.smallBlocksFilterMinHeight, justify=tk.RIGHT, selectbackground=fouColor, command=self.update_parameters)
        self.smallBlocksFilterMaxHeightLabel        = tk.Label(         self.smallBlocksFilterFrame, text='Max Height', anchor=tk.W, relief=tk.GROOVE)
        self.smallBlocksFilterMaxHeightSpinbox      = tk.Spinbox(       self.smallBlocksFilterFrame, from_=2, to_=200, textvariable=self.smallBlocksFilterMaxHeight, justify=tk.RIGHT, selectbackground=fouColor, command=self.update_parameters)

        self.smallBlocksFilterSeedLabel             = tk.Label(         self.smallBlocksFilterFrame, text='Seed (0 - 99999)', anchor=tk.W, relief=tk.GROOVE)
        self.smallBlocksFilterSeedSpinbox           = tk.Spinbox(       self.smallBlocksFilterFrame, from_=0, to_=99999, textvariable=self.smallBlocksFilterSeed, justify=tk.RIGHT, selectbackground=fouColor)
        self.smallBlocksFilterRandomSeedButton      = tk.Button(        self.smallBlocksFilterFrame, text=unicodeSymbols[0], font=('Arial', '13', 'bold'), height=1, width=3, command=lambda:self.smallBlocksFilterSeed.set(random.randint(0,99999)))
        self.smallBlocksFilterRedXtooltip           = CreateToolTip(    self.smallBlocksFilterRandomSeedButton, 'Generate random Seed between 0 and 99999')

        #Screen Lines Filter
        self.screenLinesFilterFrame                 = tk.Frame(         self.configFilterFrame, width=(confWidth-23), height=400, highlightthickness=0)

        self.screenLinesFilterLineDensityLabel      = tk.Label(         self.screenLinesFilterFrame, text='Density (%)', anchor=tk.W, relief=tk.GROOVE)
        self.screenLinesFilterLineDensitySpinbox    = tk.Spinbox(       self.screenLinesFilterFrame, from_=1, to_=99, textvariable=self.screenLinesFilterLineDensity, justify=tk.RIGHT, selectbackground=fouColor)
        self.screenLinesFilterLineDensityScale      = tk.Scale(         self.screenLinesFilterFrame, from_=1, to_=99, variable=self.screenLinesFilterLineDensity, orient=tk.HORIZONTAL, showvalue=0)
        self.screenLinesFilterLineThicknessLabel    = tk.Label(         self.screenLinesFilterFrame, text='Thickness (px)', anchor=tk.W, relief=tk.GROOVE)
        self.screenLinesFilterLineThicknessSpinbox  = tk.Spinbox(       self.screenLinesFilterFrame, from_=0, to_=9999, textvariable=self.screenLinesFilterLineThickness, justify=tk.RIGHT, selectbackground=fouColor)
        self.screenLinesFilterLineBlurLabel         = tk.Label(         self.screenLinesFilterFrame, text='Blur (px)', anchor=tk.W, relief=tk.GROOVE)
        self.screenLinesFilterLineBlurSpinbox       = tk.Spinbox(       self.screenLinesFilterFrame, from_=0, to_=9999, textvariable=self.screenLinesFilterLineBlur, justify=tk.RIGHT, selectbackground=fouColor)
        self.screenLinesFilterBlendmodeLabel        = tk.Label(         self.screenLinesFilterFrame, text='Blend Mode', anchor=tk.W, relief=tk.GROOVE)
        self.screenLinesFilterBlendmodeOptionmenu   = tk.OptionMenu(    self.screenLinesFilterFrame, self.screenLinesFilterBlendmode, *self.screenLinesFilterBlendmodeList)
        self.screenLinesFilterBlendmodeOptionmenu['menu'].config(bg=secColor)
        self.screenLinesFilterBlendmodeOptionmenu.config(bg=secColor)

        self.screenLinesFilterCheckbuttonFrame      = tk.Frame(         self.screenLinesFilterFrame)
        self.screenLinesFilterRandomCheckbutton     = tk.Checkbutton(   self.screenLinesFilterCheckbuttonFrame, text='Random', selectcolor='gray30', variable=self.screenLinesFilterRandomVar)

        self.screenLinesFilterColorFrame            = tk.Frame(         self.screenLinesFilterFrame)

        self.screenLinesFilterLineColorLabel        = tk.Label(         self.screenLinesFilterColorFrame, text='Line Color', width=43, anchor=tk.W, relief=tk.GROOVE)
        self.screenLinesFilterLineColorRedLabel     = tk.Label(         self.screenLinesFilterColorFrame, text='Red', anchor=tk.W, relief=tk.GROOVE)
        self.screenLinesFilterLineColorRedSpinbox   = tk.Spinbox(       self.screenLinesFilterColorFrame, from_=0, to_=255, textvariable=self.screenLinesFilterLineColorRed, justify=tk.RIGHT, selectbackground=fouColor)
        self.screenLinesFilterLineColorRedScale     = tk.Scale(         self.screenLinesFilterColorFrame, from_=0, to_=255, variable=self.screenLinesFilterLineColorRed, orient=tk.HORIZONTAL, showvalue=0)
        self.screenLinesFilterLineColorGreenLabel   = tk.Label(         self.screenLinesFilterColorFrame, text='Green', anchor=tk.W, relief=tk.GROOVE)
        self.screenLinesFilterLineColorGreenSpinbox = tk.Spinbox(       self.screenLinesFilterColorFrame, from_=0, to_=255, textvariable=self.screenLinesFilterLineColorGreen, justify=tk.RIGHT, selectbackground=fouColor)
        self.screenLinesFilterLineColorGreenScale   = tk.Scale(         self.screenLinesFilterColorFrame, from_=0, to_=255, variable=self.screenLinesFilterLineColorGreen, orient=tk.HORIZONTAL, showvalue=0)
        self.screenLinesFilterLineColorBlueLabel    = tk.Label(         self.screenLinesFilterColorFrame, text='Blue', anchor=tk.W, relief=tk.GROOVE)
        self.screenLinesFilterLineColorBlueSpinbox  = tk.Spinbox(       self.screenLinesFilterColorFrame, from_=0, to_=255, textvariable=self.screenLinesFilterLineColorBlue, justify=tk.RIGHT, selectbackground=fouColor)
        self.screenLinesFilterLineColorBlueScale    = tk.Scale(         self.screenLinesFilterColorFrame, from_=0, to_=255, variable=self.screenLinesFilterLineColorBlue, orient=tk.HORIZONTAL, showvalue=0)

        #Burning Noise Filter
        self.burnNoiseFilterFrame                   = tk.Frame(         self.configFilterFrame, width=(confWidth-23), height=400, highlightthickness=0)

        self.burnNoiseFilterPixelSizeLabel          = tk.Label(         self.burnNoiseFilterFrame, text='Pixel Size (px)', anchor=tk.W, relief=tk.GROOVE)
        self.burnNoiseFilterPixelSizeSpinbox        = tk.Spinbox(       self.burnNoiseFilterFrame, from_=0, to_=255, textvariable=self.burnNoiseFilterPixelSize, justify=tk.RIGHT, selectbackground=fouColor)
        self.burnNoiseFilterStretchWidthLabel       = tk.Label(         self.burnNoiseFilterFrame, text='Stretch X (%)', anchor=tk.W, relief=tk.GROOVE)
        self.burnNoiseFilterStretchWidthSpinbox     = tk.Spinbox(       self.burnNoiseFilterFrame, from_=0, to_=100, textvariable=self.burnNoiseFilterStretchWidth, justify=tk.RIGHT, selectbackground=fouColor)
        self.burnNoiseFilterStretchWidthScale       = tk.Scale(         self.burnNoiseFilterFrame, from_=0, to_=100, variable=self.burnNoiseFilterStretchWidth, orient=tk.HORIZONTAL, showvalue=0)
        self.burnNoiseFilterStretchHeightLabel      = tk.Label(         self.burnNoiseFilterFrame, text='Stretch Y (%)', anchor=tk.W, relief=tk.GROOVE)
        self.burnNoiseFilterStretchHeightSpinbox    = tk.Spinbox(       self.burnNoiseFilterFrame, from_=0, to_=100, textvariable=self.burnNoiseFilterStretchHeight, justify=tk.RIGHT, selectbackground=fouColor)
        self.burnNoiseFilterStretchHeightScale      = tk.Scale(         self.burnNoiseFilterFrame, from_=0, to_=100, variable=self.burnNoiseFilterStretchHeight, orient=tk.HORIZONTAL, showvalue=0)
        self.burnNoiseFilterDarkBrightLabel         = tk.Label(         self.burnNoiseFilterFrame, text='Value (0-255)', anchor=tk.W, relief=tk.GROOVE)
        self.rgbOffsetFilterRedXtooltip             = CreateToolTip(    self.burnNoiseFilterDarkBrightLabel, 'Sets minimum and maximum Value of the noise texture.')
        self.burnNoiseFilterDarkSpinbox             = tk.Spinbox(       self.burnNoiseFilterFrame, from_=0, to_=255, textvariable=self.burnNoiseFilterDark, justify=tk.RIGHT, selectbackground=fouColor, command=self.update_parameters)
        self.burnNoiseFilterDarkScale               = tk.Scale(         self.burnNoiseFilterFrame, from_=0, to_=255, variable=self.burnNoiseFilterDark, orient=tk.HORIZONTAL, showvalue=0)
        self.burnNoiseFilterBrightSpinbox           = tk.Spinbox(       self.burnNoiseFilterFrame, from_=1, to_=255, textvariable=self.burnNoiseFilterBright, justify=tk.RIGHT, selectbackground=fouColor, command=self.update_parameters)
        self.burnNoiseFilterBrightScale             = tk.Scale(         self.burnNoiseFilterFrame, from_=0, to_=255, variable=self.burnNoiseFilterBright, orient=tk.HORIZONTAL, showvalue=0)
        self.burnNoiseFilterContrastLabel           = tk.Label(         self.burnNoiseFilterFrame, text='Contrast (%)', anchor=tk.W, relief=tk.GROOVE)
        self.burnNoiseFilterContrastSpinbox         = tk.Spinbox(       self.burnNoiseFilterFrame, from_=0, to_=100, textvariable=self.burnNoiseFilterContrast, justify=tk.RIGHT, selectbackground=fouColor)
        self.burnNoiseFilterContrastScale           = tk.Scale(         self.burnNoiseFilterFrame, from_=0, to_=100, variable=self.burnNoiseFilterContrast, orient=tk.HORIZONTAL, showvalue=0)
        self.burnNoiseFilterIntensityLabel          = tk.Label(         self.burnNoiseFilterFrame, text='Intensity (%)', anchor=tk.W, relief=tk.GROOVE)
        self.burnNoiseFilterIntensitySpinbox        = tk.Spinbox(       self.burnNoiseFilterFrame, from_=0, to_=100, textvariable=self.burnNoiseFilterIntensity, justify=tk.RIGHT, selectbackground=fouColor)
        self.burnNoiseFilterIntensityScale          = tk.Scale(         self.burnNoiseFilterFrame, from_=0, to_=100, variable=self.burnNoiseFilterIntensity, orient=tk.HORIZONTAL, showvalue=0)
        self.burnNoiseFilterBlurLabel               = tk.Label(         self.burnNoiseFilterFrame, text='Blur (px)', anchor=tk.W, relief=tk.GROOVE)
        self.burnNoiseFilterBlurSpinbox             = tk.Spinbox(       self.burnNoiseFilterFrame, from_=0, to_=9999, textvariable=self.burnNoiseFilterBlur, justify=tk.RIGHT, selectbackground=fouColor)
        
        self.burnNoiseFilterCheckbuttonFrame        = tk.Frame(         self.burnNoiseFilterFrame)
        self.burnNoiseFilterInvertCheckbutton       = tk.Checkbutton(   self.burnNoiseFilterCheckbuttonFrame, text='Invert', selectcolor='gray30', variable=self.burnNoiseFilterInvert)  
        self.burnNoiseFilterColorCheckbutton        = tk.Checkbutton(   self.burnNoiseFilterCheckbuttonFrame, text='Colored', selectcolor='gray30', variable=self.burnNoiseFilterColor)  
        self.burnNoiseFilterSeedLabel               = tk.Label(         self.burnNoiseFilterFrame, text='Seed (0 - 99999)', anchor=tk.W, relief=tk.GROOVE)
        self.burnNoiseFilterSeedSpinbox             = tk.Spinbox(       self.burnNoiseFilterFrame, from_=0, to_=99999, textvariable=self.burnNoiseFilterSeed, justify=tk.RIGHT, selectbackground=fouColor)
        self.burnNoiseFilterRandomSeedButton        = tk.Button(        self.burnNoiseFilterFrame, text=unicodeSymbols[0], font=('Arial', '13', 'bold'), height=1, width=3, command=lambda:self.burnNoiseFilterSeed.set(random.randint(0,99999)))
        self.burnNoiseFilterRedXtooltip             = CreateToolTip(    self.burnNoiseFilterRandomSeedButton, 'Generate random Seed between 0 and 99999')

        #RGB Screen Filter
        #self.rgbScreenFilterScrollbar               = tk.Scrollbar(     self.configFilterFrame, orient=tk.VERTICAL)
        #self.rgbScreenFilterCanvas                  = tk.Canvas(        self.configFilterFrame, yscrollcommand=self.rgbScreenFilterScrollbar.set, highlightthickness=0)
        #self.rgbScreenFilterScrollbar.config(command=self.rgbScreenFilterCanvas.yview)
        #self.rgbScreenFilterCanvas.bind_all("<MouseWheel>", lambda event: self.rgbScreenFilterCanvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        self.rgbScreenFilterFrame                   = tk.Frame(         self.configFilterFrame)
        #self.rgbScreenFilterCanvas.create_window(0,0, window=self.rgbScreenFilterFrame, anchor=tk.NW)

        self.rgbScreenFilterPixelSizeLabel          = tk.Label(         self.rgbScreenFilterFrame, text='Pixel Size (px)', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterPixelSizeSpinbox        = tk.Spinbox(       self.rgbScreenFilterFrame, from_=3, to_=255, width=5, textvariable=self.rgbScreenFilterPixelSize, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterPixelGapLabel           = tk.Label(         self.rgbScreenFilterFrame, text='Pixel Gap (px)', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterPixelGapSpinbox         = tk.Spinbox(       self.rgbScreenFilterFrame, from_=1, to_=255, textvariable=self.rgbScreenFilterPixelGap, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterIntensityLabel          = tk.Label(         self.rgbScreenFilterFrame, text='Intensity (%)', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterIntensitySpinbox        = tk.Spinbox(       self.rgbScreenFilterFrame, from_=0, to_=100, textvariable=self.rgbScreenFilterIntensity, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterIntensityScale          = tk.Scale(         self.rgbScreenFilterFrame, from_=0, to_=100, variable=self.rgbScreenFilterIntensity, showvalue=0, orient=tk.HORIZONTAL)
        self.rgbScreenFilterBlurLabel               = tk.Label(         self.rgbScreenFilterFrame, text='Blur (px)', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterBlurSpinbox             = tk.Spinbox(       self.rgbScreenFilterFrame, from_=0, to_=100, textvariable=self.rgbScreenFilterBlur, justify=tk.RIGHT, selectbackground=fouColor)
        
        self.rgbScreenFilterColorFrame              = tk.Frame(         self.rgbScreenFilterFrame)#, bg='gray30')

        self.rgbScreenFilterFirstColorLabel         = tk.Label(         self.rgbScreenFilterColorFrame, text='First Color', width=43, anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterFirstRedLabel           = tk.Label(         self.rgbScreenFilterColorFrame, text='Red', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterFirstRedSpinbox         = tk.Spinbox(       self.rgbScreenFilterColorFrame, from_=0, to_=255, textvariable=self.rgbScreenFilterFirstRed, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterFirstRedScale           = tk.Scale(         self.rgbScreenFilterColorFrame, from_=0, to_=255, variable=self.rgbScreenFilterFirstRed, showvalue=0, orient=tk.HORIZONTAL)
        self.rgbScreenFilterFirstGreenLabel         = tk.Label(         self.rgbScreenFilterColorFrame, text='Green', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterFirstGreenSpinbox       = tk.Spinbox(       self.rgbScreenFilterColorFrame, from_=0, to_=255, textvariable=self.rgbScreenFilterFirstGreen, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterFirstGreenScale         = tk.Scale(         self.rgbScreenFilterColorFrame, from_=0, to_=255, variable=self.rgbScreenFilterFirstGreen, showvalue=0, orient=tk.HORIZONTAL)
        self.rgbScreenFilterFirstBlueLabel          = tk.Label(         self.rgbScreenFilterColorFrame, text='Blue', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterFirstBlueSpinbox        = tk.Spinbox(       self.rgbScreenFilterColorFrame, from_=0, to_=255, textvariable=self.rgbScreenFilterFirstBlue, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterFirstBlueScale          = tk.Scale(         self.rgbScreenFilterColorFrame, from_=0, to_=255, variable=self.rgbScreenFilterFirstBlue, showvalue=0, orient=tk.HORIZONTAL)

        self.rgbScreenFilterSecondColorLabel        = tk.Label(         self.rgbScreenFilterColorFrame, text='Second Color', width=43, anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterSecondRedLabel          = tk.Label(         self.rgbScreenFilterColorFrame, text='Red', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterSecondRedSpinbox        = tk.Spinbox(       self.rgbScreenFilterColorFrame, from_=0, to_=255, textvariable=self.rgbScreenFilterSecondRed, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterSecondRedScale          = tk.Scale(         self.rgbScreenFilterColorFrame, from_=0, to_=255, variable=self.rgbScreenFilterSecondRed, showvalue=0, orient=tk.HORIZONTAL)
        self.rgbScreenFilterSecondGreenLabel        = tk.Label(         self.rgbScreenFilterColorFrame, text='Green', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterSecondGreenSpinbox      = tk.Spinbox(       self.rgbScreenFilterColorFrame, from_=0, to_=255, textvariable=self.rgbScreenFilterSecondGreen, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterSecondGreenScale        = tk.Scale(         self.rgbScreenFilterColorFrame, from_=0, to_=255, variable=self.rgbScreenFilterSecondGreen, showvalue=0, orient=tk.HORIZONTAL)
        self.rgbScreenFilterSecondBlueLabel         = tk.Label(         self.rgbScreenFilterColorFrame, text='Blue', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterSecondBlueSpinbox       = tk.Spinbox(       self.rgbScreenFilterColorFrame, from_=0, to_=255, textvariable=self.rgbScreenFilterSecondBlue, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterSecondBlueScale         = tk.Scale(         self.rgbScreenFilterColorFrame, from_=0, to_=255, variable=self.rgbScreenFilterSecondBlue, showvalue=0, orient=tk.HORIZONTAL)
        
        self.rgbScreenFilterThirdColorLabel         = tk.Label(         self.rgbScreenFilterColorFrame, text='Third Color', width=43, anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterThirdRedLabel           = tk.Label(         self.rgbScreenFilterColorFrame, text='Red', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterThirdRedSpinbox         = tk.Spinbox(       self.rgbScreenFilterColorFrame, from_=0, to_=255, textvariable=self.rgbScreenFilterThirdRed, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterThirdRedScale           = tk.Scale(         self.rgbScreenFilterColorFrame, from_=0, to_=255, variable=self.rgbScreenFilterThirdRed, showvalue=0, orient=tk.HORIZONTAL)
        self.rgbScreenFilterThirdGreenLabel         = tk.Label(         self.rgbScreenFilterColorFrame, text='Green', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterThirdGreenSpinbox       = tk.Spinbox(       self.rgbScreenFilterColorFrame, from_=0, to_=255, textvariable=self.rgbScreenFilterThirdGreen, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterThirdGreenScale         = tk.Scale(         self.rgbScreenFilterColorFrame, from_=0, to_=255, variable=self.rgbScreenFilterThirdGreen, showvalue=0, orient=tk.HORIZONTAL)
        self.rgbScreenFilterThirdBlueLabel          = tk.Label(         self.rgbScreenFilterColorFrame, text='Blue', anchor=tk.W, relief=tk.GROOVE)
        self.rgbScreenFilterThirdBlueSpinbox        = tk.Spinbox(       self.rgbScreenFilterColorFrame, from_=0, to_=255, textvariable=self.rgbScreenFilterThirdBlue, justify=tk.RIGHT, selectbackground=fouColor)
        self.rgbScreenFilterThirdBlueScale          = tk.Scale(         self.rgbScreenFilterColorFrame, from_=0, to_=255, variable=self.rgbScreenFilterThirdBlue, showvalue=0, orient=tk.HORIZONTAL)

        ###positon widgets****************************************************************************************
        ##Frames
        #Image Frame Setup
        self.imageFrame.grid(               column=0, row=0, rowspan=2)
        self.imageLabelFrame.grid(          column=0, row=0)
        self.imageCanvas.grid(              column=0, row=0)
        self.imageCanvas.create_text(375, 375, text='Open an Image', font=('Helvetica', '42'), fill='yellow', anchor=tk.CENTER)
        self.imageProgressbar.grid(         column=0, row=1, pady=1)

        #Config Frame Setup
        self.configFrame.grid(              column=1, row=0, sticky=tk.W+tk.N+tk.E)

        self.topConfigFrame.grid(           column=0, row=0, sticky=tk.W)

        self.configFilterFrame.grid(        column=0, row=1, sticky=tk.W+tk.N+tk.N+tk.S)
        self.configFilterFrame.grid_rowconfigure(0, weight=1)
        self.configFilterFrame.grid_columnconfigure(0, weight=1)
        self.configFilterFrame.grid_propagate(0)

        self.bottomConfigFrame.grid(        column=0, row=2, sticky=tk.E+tk.S)

        #Top Config Frame
        self.filterListListbox.grid(        column=0, row=0, pady=10, padx=1, rowspan=2, sticky=tk.E+tk.W)
        self.filterListScrollbar.grid(      column=1, row=0, pady=12, padx=0, rowspan=2, sticky=tk.N+tk.S+tk.W)
        self.filterListButton.grid(         column=2, row=0, pady=2 , padx=5, sticky=tk.SW)
        self.presetListButton.grid(         column=2, row=1, pady=2 , padx=5, sticky=tk.NW)

        #Bottom Config Frame 
        self.previewButton.grid(            column=1, row=0, padx=2, pady=2, sticky=tk.E, columnspan=2)
        self.randomButton.grid(             column=1, row=1, padx=2, pady=2, sticky=tk.SE)
        self.renderButton.grid(             column=2, row=1, padx=2, pady=2, sticky=tk.SE)
        self.previewActiveCheckbutton.grid( column=0, row=1, padx=2, pady=2, sticky=tk.E)
       
    def switch_filter_options(self, event):
        if self.filterListListbox.curselection():
            try:
                #Gets Name of the selected Filter as a String
                selectedFilter = self.filterList[int(' '.join(map(str, self.filterListListbox.curselection())))]

                #Clears Filterconfig-Frame
                for child in self.configFilterFrame.winfo_children():
                    child.grid_forget()

                #Looks for active Filter Configuration and positions widgets
                if selectedFilter == 'RGB Offset':
                    self.rgbOffsetFilterCanvas.grid(                    column=0, row=0, padx=0, pady=3, sticky=tk.NW)
                    self.rgbOffsetFilterCanvas.grid_propagate(0)

                    self.rgbOffsetFilterRedXlabel.grid(                 column=0, row=0, padx=2, pady=2, sticky=tk.W)
                    self.rgbOffsetFilterRedXscale.grid(                 column=1, row=0, padx=2, pady=2, sticky=tk.E)
                    self.rgbOffsetFilterRedYlabel.grid(                 column=0, row=1, padx=2, pady=2, sticky=tk.W)
                    self.rgbOffsetFilterRedYscale.grid(                 column=1, row=1, padx=2, pady=2, sticky=tk.E)
                    self.rgbOffsetFilterGreenXlabel.grid(               column=0, row=2, padx=2, pady=2, sticky=tk.W)
                    self.rgbOffsetFilterGreenXscale.grid(               column=1, row=2, padx=2, pady=2, sticky=tk.E)
                    self.rgbOffsetFilterGreenYlabel.grid(               column=0, row=3, padx=2, pady=2, sticky=tk.W)
                    self.rgbOffsetFilterGreenYscale.grid(               column=1, row=3, padx=2, pady=2, sticky=tk.E)
                    self.rgbOffsetFilterBlueXlabel.grid(                column=0, row=4, padx=2, pady=2, sticky=tk.W)
                    self.rgbOffsetFilterBlueXscale.grid(                column=1, row=4, padx=2, pady=2, sticky=tk.E)
                    self.rgbOffsetFilterBlueYlabel.grid(                column=0, row=5, padx=2, pady=2, sticky=tk.W)
                    self.rgbOffsetFilterBlueYscale.grid(                column=1, row=5, padx=2, pady=2, sticky=tk.E)

                    self.rgbOffsetFilterBottomFrame.grid(               column=0, row=6, padx=1, pady=0, sticky=tk.W, columnspan=2)
                    self.rgbOffsetFilterBetterCheckButton.grid(         column=0, row=0, padx=1, pady=0, sticky=tk.W)
                    self.rgbOffsetFilterRandomButton.grid(              column=1, row=0, padx=3, pady=2, sticky=tk.W)

                if selectedFilter == 'Big Blocks':  
                    self.bigBlocksFilterFrame.grid(                     column=0, row=0, padx=0, pady=3, sticky=tk.NW)

                    self.bigBlocksFilterBlockCountLabel.grid(           column=0, row=0, padx=2, pady=2, sticky=tk.W)
                    self.bigBlocksFilterBlockCountSpinbox.grid(         column=1, row=0, padx=2, pady=2, sticky=tk.W)
                    self.bigBlocksFilterBlockMaxHeightLabel.grid(       column=0, row=1, padx=2, pady=2, sticky=tk.W)
                    self.bigBlocksFilterBlockMaxHeightSpinbox.grid(     column=1, row=1, padx=2, pady=2, sticky=tk.W)
                    self.bigBlocksFilterBlockMaxOffsetLabel.grid(       column=0, row=2, padx=2, pady=2, sticky=tk.W)
                    self.bigBlocksFilterBlockMaxOffsetSpinbox.grid(     column=1, row=2, padx=2, pady=2, sticky=tk.W)
                    self.bigBlocksFilterBlockMaxOffsetScale.grid(       column=2, row=2, padx=2, pady=2, sticky=tk.W)
                    self.bigBlocksFilterSeedLabel.grid(                 column=0, row=3, padx=2, pady=2, sticky=tk.W)
                    self.bigBlocksFilterSeedSpinbox.grid(               column=1, row=3, padx=2, pady=2, sticky=tk.W)
                    self.bigBlocksFilterRandomSeedButton.grid(          column=2, row=3, padx=2, pady=2, sticky=tk.W)

                if selectedFilter == 'Small Blocks':
                    self.smallBlocksFilterFrame.grid(                   column=0, row=0, padx=0, pady=3, sticky=tk.NW)

                    self.smallBlocksFilterBlockCountLabel.grid(         column=0, row=0, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterBlockCountSpinbox.grid(       column=1, row=0, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterMinWidthLabel.grid(           column=0, row=1, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterMinWidthSpinbox.grid(         column=1, row=1, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterMaxWidthLabel.grid(           column=0, row=2, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterMaxWidthSpinbox.grid(         column=1, row=2, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterMinHeightLabel.grid(          column=0, row=3, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterMinHeightSpinbox.grid(        column=1, row=3, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterMaxHeightLabel.grid(          column=0, row=4, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterMaxHeightSpinbox.grid(        column=1, row=4, padx=2, pady=2, sticky=tk.W)

                    self.smallBlocksFilterSeedLabel.grid(              column=0, row=5, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterSeedSpinbox.grid(             column=1, row=5, padx=2, pady=2, sticky=tk.W)
                    self.smallBlocksFilterRandomSeedButton.grid(        column=2, row=5, padx=2, pady=2, sticky=tk.W)

                if selectedFilter == 'Screen Lines':
                    self.screenLinesFilterFrame.grid(              column=0, row=0, padx=0, pady=3, sticky=tk.NW)

                    self.screenLinesFilterLineDensityLabel.grid(        column=0, row=0, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterLineDensitySpinbox.grid(      column=1, row=0, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterLineDensityScale.grid(        column=2, row=0, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterLineThicknessLabel.grid(      column=0, row=1, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterLineThicknessSpinbox.grid(    column=1, row=1, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterLineBlurLabel.grid(           column=0, row=2, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterLineBlurSpinbox.grid(         column=1, row=2, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterBlendmodeLabel.grid(          column=0, row=3, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterBlendmodeOptionmenu.grid(     column=1, row=3, padx=0, pady=2, sticky=tk.W, columnspan=2)

                    self.screenLinesFilterCheckbuttonFrame.grid(        column=0, row=4, padx=2, pady=2, sticky=tk.W, columnspan=3)
                    self.screenLinesFilterRandomCheckbutton.grid(       column=0, row=0, padx=0, pady=2, sticky=tk.W)

                    self.screenLinesFilterColorFrame.grid(              column=0, row=5, padx=2, pady=2, columnspan=3, sticky=tk.N)

                    self.screenLinesFilterLineColorLabel.grid(          column=0, row=1, padx=2, pady=2, sticky=tk.W, columnspan=3)
                    self.screenLinesFilterLineColorRedLabel.grid(       column=0, row=2, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterLineColorRedSpinbox.grid(     column=1, row=2, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterLineColorRedScale.grid(       column=2, row=2, padx=2, pady=4, sticky=tk.W)
                    self.screenLinesFilterLineColorGreenLabel.grid(     column=0, row=3, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterLineColorGreenSpinbox.grid(   column=1, row=3, padx=2, pady=2, sticky=tk.W)
                    self.screenLinesFilterLineColorGreenScale.grid(     column=2, row=3, padx=2, pady=4, sticky=tk.W)
                    self.screenLinesFilterLineColorBlueLabel.grid(      column=0, row=4, padx=2, pady=4, sticky=tk.W)
                    self.screenLinesFilterLineColorBlueSpinbox.grid(    column=1, row=4, padx=2, pady=4, sticky=tk.W)
                    self.screenLinesFilterLineColorBlueScale.grid(      column=2, row=4, padx=2, pady=4, sticky=tk.W)

                if selectedFilter == 'Burning Noise':
                    self.burnNoiseFilterFrame.grid(                column=0, row=0, padx=0, pady=3, sticky=tk.NW)

                    self.burnNoiseFilterPixelSizeLabel.grid(            column=0, row=0, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterPixelSizeSpinbox.grid(          column=1, row=0, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterStretchWidthLabel.grid(         column=0, row=1, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterStretchWidthSpinbox.grid(       column=1, row=1, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterStretchWidthScale.grid(         column=2, row=1, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterStretchHeightLabel.grid(        column=0, row=2, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterStretchHeightSpinbox.grid(      column=1, row=2, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterStretchHeightScale.grid(        column=2, row=2, padx=2, pady=2, sticky=tk.W)

                    self.burnNoiseFilterDarkBrightLabel.grid(           column=0, row=3, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterDarkSpinbox.grid(               column=1, row=3, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterBrightSpinbox.grid(             column=2, row=3, padx=2, pady=2, sticky=tk.W)

                    self.burnNoiseFilterContrastLabel.grid(             column=0, row=4, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterContrastSpinbox.grid(           column=1, row=4, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterContrastScale.grid(             column=2, row=4, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterIntensityLabel.grid(            column=0, row=5, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterIntensitySpinbox.grid(          column=1, row=5, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterIntensityScale.grid(            column=2, row=5, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterBlurLabel.grid(                 column=0, row=6, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterBlurSpinbox.grid(               column=1, row=6, padx=2, pady=2, sticky=tk.W)

                    self.burnNoiseFilterCheckbuttonFrame.grid(          column=0, row=7, padx=2, pady=2, sticky=tk.W, columnspan=3)
                    self.burnNoiseFilterInvertCheckbutton.grid(         column=0, row=0, padx=0, pady=0, sticky=tk.W)
                    self.burnNoiseFilterColorCheckbutton.grid(          column=1, row=0, padx=0, pady=0, sticky=tk.W)

                    self.burnNoiseFilterSeedLabel.grid(                 column=0, row=8, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterSeedSpinbox.grid(               column=1, row=8, padx=2, pady=2, sticky=tk.W)
                    self.burnNoiseFilterRandomSeedButton.grid(          column=2, row=8, padx=2, pady=2, sticky=tk.W)

                if selectedFilter == 'RGB Screen':
                    #self.rgbScreenFilterCanvas.grid(                column=0, row=0, padx=0, pady=3, sticky='new')
                    self.rgbScreenFilterFrame.grid(                     column=0, row=0, padx=0, pady=3, sticky='new')

                    self.rgbScreenFilterPixelSizeLabel.grid(            column=0, row=0, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterPixelSizeSpinbox.grid(          column=1, row=0, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterPixelGapLabel.grid(             column=0, row=1, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterPixelGapSpinbox.grid(           column=1, row=1, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterIntensityLabel.grid(            column=0, row=2, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterIntensitySpinbox.grid(          column=1, row=2, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterIntensityScale.grid(            column=2, row=2, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterBlurLabel.grid(                 column=0, row=3, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterBlurSpinbox.grid(               column=1, row=3, padx=2, pady=2, sticky=tk.W)

                    self.rgbScreenFilterColorFrame.grid(                column=0, row=4, padx=0, pady=8, sticky=tk.W, columnspan=3)

                    self.rgbScreenFilterFirstColorLabel.grid(           column=0, row=0, padx=2, pady=2, sticky=tk.W, columnspan=3)
                    self.rgbScreenFilterFirstRedLabel.grid(             column=0, row=1, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterFirstRedSpinbox.grid(           column=1, row=1, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterFirstRedScale.grid(             column=2, row=1, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterFirstGreenLabel.grid(           column=0, row=2, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterFirstGreenSpinbox.grid(         column=1, row=2, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterFirstGreenScale.grid(           column=2, row=2, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterFirstBlueLabel.grid(            column=0, row=3, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterFirstBlueSpinbox.grid(          column=1, row=3, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterFirstBlueScale.grid(            column=2, row=3, padx=2, pady=2, sticky=tk.W)

                    self.rgbScreenFilterSecondColorLabel.grid(          column=0, row=4, padx=2, pady=2, sticky=tk.W, columnspan=3)
                    self.rgbScreenFilterSecondRedLabel.grid(            column=0, row=5, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterSecondRedSpinbox.grid(          column=1, row=5, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterSecondRedScale.grid(            column=2, row=5, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterSecondGreenLabel.grid(          column=0, row=6, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterSecondGreenSpinbox.grid(        column=1, row=6, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterSecondGreenScale.grid(          column=2, row=6, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterSecondBlueLabel.grid(           column=0, row=7, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterSecondBlueSpinbox.grid(         column=1, row=7, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterSecondBlueScale.grid(           column=2, row=7, padx=2, pady=2, sticky=tk.W)

                    self.rgbScreenFilterThirdColorLabel.grid(           column=0, row=8, padx=2, pady=2, sticky=tk.W, columnspan=3)
                    self.rgbScreenFilterThirdRedLabel.grid(             column=0, row=9, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterThirdRedSpinbox.grid(           column=1, row=9, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterThirdRedScale.grid(             column=2, row=9, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterThirdGreenLabel.grid(           column=0, row=10, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterThirdGreenSpinbox.grid(         column=1, row=10, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterThirdGreenScale.grid(           column=2, row=10, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterThirdBlueLabel.grid(            column=0, row=11, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterThirdBlueSpinbox.grid(          column=1, row=11, padx=2, pady=2, sticky=tk.W)
                    self.rgbScreenFilterThirdBlueScale.grid(            column=2, row=11, padx=2, pady=2, sticky=tk.W)

                    #self.update_idletasks()

                    #self.rgbScreenFilterCanvas.config(height=self.configFilterFrame.winfo_height(),scrollregion=(0,0,self.configFilterFrame.winfo_width(), self.configFilterFrame.winfo_height()))
                    #self.rgbScreenFilterScrollbar.grid(column=1, row=0, padx=1, sticky=tk.N+tk.S+tk.W)
            except:
                glitchLogger.exception('Filter Options failed to update!')
                showerror('Error', 'Filter Options failed to update!')

    def browse_file(self, event=None):
        tempSourceImagePath = ''
        tempSourceImagePath = filedialog.askopenfilename(initialdir='/', title='Open Image...', defaultextension=self.sourceImageExtension, **self.FILEOPTIONS)

        if tempSourceImagePath and self.continue_without_save():
            try:
                filename, self.sourceImageExtension = os.path.splitext(tempSourceImagePath)
                del filename
                self.sourceImagePath = tempSourceImagePath
                self.sourceImage = Image.open(self.sourceImagePath)
            except:
                glitchLogger.exception('Loading Image failed! - Filepath: ', tempSourceImagePath)
                showerror('Error', 'Loading Image failed! - Filepath:\n{}'.format(tempSourceImagePath))
                self.sourceImagePath = ''
            else:
                self.sourceImage.load()
                self.firstImageLoaded = True
                self.sourceImage = self.sourceImage.convert('RGB')
                self.tempImage = copy.deepcopy(self.sourceImage)

                #Create and Load Thumbnail
                self.update_preview()

                #Set Parameters
                self.update_parameters()

    def update_parameters(self):
        try:
            #RGB Offset Filter
            self.rgbOffsetFilterRedXscale.config(to_=self.tempImage.width)
            self.rgbOffsetFilterBlueXscale.config(to_=self.tempImage.width)
            self.rgbOffsetFilterGreenXscale.config(to_=self.tempImage.width)
            self.rgbOffsetFilterRedYscale.config(to_=self.tempImage.height)
            self.rgbOffsetFilterBlueYscale.config(to_=self.tempImage.height)
            self.rgbOffsetFilterGreenYscale.config(to_=self.tempImage.height)

            self.rgbOffsetFilterRedXscale.config(from_=-self.tempImage.width)
            self.rgbOffsetFilterBlueXscale.config(from_=-self.tempImage.width)
            self.rgbOffsetFilterGreenXscale.config(from_=-self.tempImage.width)
            self.rgbOffsetFilterRedYscale.config(from_=-self.tempImage.height)
            self.rgbOffsetFilterBlueYscale.config(from_=-self.tempImage.height)
            self.rgbOffsetFilterGreenYscale.config(from_=-self.tempImage.height)

            #Big Blocks Filter
            self.bigBlocksFilterBlockMaxHeight.set(((self.tempImage.height)/100)*(100/self.bigBlocksFilterBlockCountVar.get()))
            self.bigBlocksFilterBlockMaxHeightSpinbox.config(to_=(self.bigBlocksFilterBlockMaxHeight.get()))

            #Small Blocks Filter
            self.smallBlocksFilterMaxHeightSpinbox.config(to_=self.tempImage.height)
            self.smallBlocksFilterMaxWidthSpinbox.config(to_=self.tempImage.width)
            if self.smallBlocksFilterMaxHeight.get() <= self.smallBlocksFilterMinHeight.get():
                self.smallBlocksFilterMinHeight.set(self.smallBlocksFilterMaxHeight.get()-1)
            if self.smallBlocksFilterMaxWidth.get() <= self.smallBlocksFilterMinWidth.get():
                self.smallBlocksFilterMinWidth.set(self.smallBlocksFilterMaxWidth.get()-1)

            #Burning Noise Filter
            if self.burnNoiseFilterDark.get() >= self.burnNoiseFilterBright.get():
                self.burnNoiseFilterDark.set(self.burnNoiseFilterBright.get()-1)

            #Screen Lines Filter
            self.screenLinesFilterLineThicknessSpinbox.config(to_=self.sourceImage.height/2)
        except:
            glitchLogger.exception('Updating parameters failed!')
            showerror('Error', 'Updating parameters failed!')

    def update_labels(self, *args):
        if self.setupFinished:
            try:
                #RGB Screen Filter
                color = '#%02x%02x%02x' % (self.rgbScreenFilterFirstRed.get(), self.rgbScreenFilterFirstGreen.get(), self.rgbScreenFilterFirstBlue.get())
                self.rgbScreenFilterFirstColorLabel.configure(bg=color)
                if ((self.rgbScreenFilterFirstRed.get() + self.rgbScreenFilterFirstGreen.get() + self.rgbScreenFilterFirstBlue.get())/3) > 127:
                    self.rgbScreenFilterFirstColorLabel.configure(fg='black')
                else:
                    self.rgbScreenFilterFirstColorLabel.configure(fg='white')

                color = '#%02x%02x%02x' % (self.rgbScreenFilterSecondRed.get(), self.rgbScreenFilterSecondGreen.get(), self.rgbScreenFilterSecondBlue.get())
                self.rgbScreenFilterSecondColorLabel.configure(bg=color)
                if ((self.rgbScreenFilterSecondRed.get() + self.rgbScreenFilterSecondGreen.get() + self.rgbScreenFilterSecondBlue.get())/3) > 127:
                    self.rgbScreenFilterSecondColorLabel.configure(fg='black')
                else:
                    self.rgbScreenFilterSecondColorLabel.configure(fg='white')

                color = '#%02x%02x%02x' % (self.rgbScreenFilterThirdRed.get(), self.rgbScreenFilterThirdGreen.get(), self.rgbScreenFilterThirdBlue.get())
                self.rgbScreenFilterThirdColorLabel.configure(bg=color)
                if ((self.rgbScreenFilterThirdRed.get() + self.rgbScreenFilterThirdGreen.get() + self.rgbScreenFilterThirdBlue.get())/3) > 127:
                    self.rgbScreenFilterThirdColorLabel.configure(fg='black')
                else:
                    self.rgbScreenFilterThirdColorLabel.configure(fg='white')

                color = '#%02x%02x%02x' % (self.screenLinesFilterLineColorRed.get(), self.screenLinesFilterLineColorGreen.get(), self.screenLinesFilterLineColorBlue.get())
                self.screenLinesFilterLineColorLabel.configure(bg=color)
                if ((self.screenLinesFilterLineColorRed.get() + self.screenLinesFilterLineColorGreen.get() + self.screenLinesFilterLineColorBlue.get())/3) > 127:
                    self.screenLinesFilterLineColorLabel.configure(fg='black')
                else:
                    self.screenLinesFilterLineColorLabel.configure(fg='white')
            except:
                glitchLogger.exception('Update of labels failed!')

    def save_image(self, event=None):
        if self.firstImageLoaded:
            try:
                filename, extension = os.path.splitext(self.sourceImagePath)
                self.tempImage.save('{}{}{}'.format(filename, '-GlitchFilter', extension))
                self.isImageSaved = True
            except:
                glitchLogger.exception('Saveing Image failed!')
                showerror('Error', 'Saveing Image failed! - Filepath:\n{}{}{}'.format(filename, '-GlitchFilter', extension))

    def save_image_as(self, event=None):
        tempFilePath = ''
        if self.firstImageLoaded:
            filepath, extension = os.path.splitext(self.sourceImagePath)
            print(self.sourceImageExtension)
            tempFilePath = filedialog.asksaveasfilename(initialdir=filepath, title='Save Image...', defaultextension=self.sourceImageExtension, **self.FILEOPTIONS)
        try:
            if tempFilePath:
                self.tempImage.save(tempFilePath)
                self.isImageSaved = True
        except:
            glitchLogger.exception('Saveing Image failed!')
            showerror('Error', 'Saveing Image failed! - Filepath:\n{}'.format(tempFilePath))

    def create_thumbnail(self, image):
        try:
            tempThumbImage = copy.deepcopy(image)
            tempThumbImage.load()

            thumbnailWidth  = tempThumbImage.width
            thumbnailHeight = tempThumbImage.height
            scaleX = self.imageCanvas.winfo_width()  / thumbnailWidth
            scaleY = self.imageCanvas.winfo_height() / thumbnailHeight

            if(scaleX <= scaleY):                                    
                thumbnailWidth  = int(thumbnailWidth  * scaleX)  
                thumbnailHeight = int(thumbnailHeight * scaleX)    

            if(scaleX > scaleY):                                    
                thumbnailWidth  = int(thumbnailWidth  * scaleY)    
                thumbnailHeight = int(thumbnailHeight * scaleY)

            tempThumbImage = tempThumbImage.resize((int(thumbnailWidth), int(thumbnailHeight)), Image.LANCZOS)
            self.thumbImage = ImageTk.PhotoImage(tempThumbImage)
            canvasPosX = int((self.imageCanvas.winfo_width()  - self.thumbImage.width() + 2)/2)
            canvasPosY = int((self.imageCanvas.winfo_height() - self.thumbImage.height() + 2)/2)

            self.imageCanvas.delete('all')
            self.imageCanvas.config(bg=bgColor)
            self.imageCanvas.create_image(canvasPosX, canvasPosY, image=self.thumbImage, anchor=tk.N+tk.W)
        except:
            glitchLogger.exception('Creation of thumbnail failed!')
            showerror('Error', 'Creation of thumbnail failed!')

    def refresh_filter(self):
        try:
            #RGB Offset
            if self.rgbOffsetFilterActiveState.get():
                for child in self.rgbOffsetFilterCanvas.winfo_children():
                    try:
                        child.configure(state='normal')
                    except:
                        pass
                for child in self.rgbOffsetFilterBottomFrame.winfo_children():
                    try:
                        child.configure(state='normal')
                    except:
                        pass
            else:
                for child in self.rgbOffsetFilterCanvas.winfo_children():
                    try:
                        child.configure(state='disable')
                    except:
                        pass
                for child in self.rgbOffsetFilterBottomFrame.winfo_children():
                    try:
                        child.configure(state='disable')
                    except:
                        pass

            #Big Blocks Offset
            if self.bigBlocksFilterActiveState.get():
                for child in self.bigBlocksFilterFrame.winfo_children():
                    child.configure(state='normal')
            else:
                for child in self.bigBlocksFilterFrame.winfo_children():
                    child.configure(state='disable')

            #Small Blocks Offset
            if self.smallBlocksFilterActiveState.get():
                for child in self.smallBlocksFilterFrame.winfo_children():
                    child.configure(state='normal')
            else:
                for child in self.smallBlocksFilterFrame.winfo_children():
                    child.configure(state='disable')

            #Screen Lines
            if self.screenLinesFilterActiveState.get():
                for child in self.screenLinesFilterFrame.winfo_children():
                    try:
                        child.configure(state='normal')
                    except:
                        pass
                for child in self.screenLinesFilterCheckbuttonFrame.winfo_children():
                    child.configure(state='normal')
                for child in self.screenLinesFilterColorFrame.winfo_children():
                    child.configure(state='normal')
            else:
                for child in self.screenLinesFilterFrame.winfo_children():
                    try:
                        child.configure(state='disable')
                    except:
                        pass
                for child in self.screenLinesFilterCheckbuttonFrame.winfo_children():
                    child.configure(state='disable')
                for child in self.screenLinesFilterColorFrame.winfo_children():
                    child.configure(state='disable')

            #Burning Noise
            if self.burnNoiseFilterActiveState.get():
                for child in self.burnNoiseFilterFrame.winfo_children():
                    try:
                        child.configure(state='normal')
                    except:
                        pass
                for child in self.burnNoiseFilterCheckbuttonFrame.winfo_children():
                    child.configure(state='normal')
            else:
                for child in self.burnNoiseFilterFrame.winfo_children():
                    try:
                        child.configure(state='disable')
                    except:
                        pass
                for child in self.burnNoiseFilterCheckbuttonFrame.winfo_children():
                    child.configure(state='disable')

            #RGB Screen
            if self.rgbScreenFilterActiveState.get():
                for child in self.rgbScreenFilterFrame.winfo_children():
                    try:
                        child.configure(state='normal')
                    except:
                        pass
                for child in self.rgbScreenFilterColorFrame.winfo_children():
                    try:
                        child.configure(state='normal')
                    except:
                        pass
            else:
                for child in self.rgbScreenFilterFrame.winfo_children():
                    try:
                        child.configure(state='disable')
                    except:
                        pass
                for child in self.rgbScreenFilterColorFrame.winfo_children():
                    try:
                        child.configure(state='disable')
                    except:
                        pass
        except:
            glitchLogger.exception('Refresh of filter failed!')
            showerror('Refresh of filter failed!')

    def update_preview(self):
        if self.firstImageLoaded:
            if self.previewActiveVar.get():
                self.create_thumbnail(self.tempImage)   #Displays altered Image
            else:
                self.create_thumbnail(self.sourceImage) #Displays source Image

    def apply_changes(self):
        self.filterThread = threading.Thread(target=self.apply_filters)     #Creates thread for the application of the filters
        self.filterThread.daemon = True                                     # -> progressbar wouldn't update without more configuration
        for child in self.bottomConfigFrame.winfo_children():
            try:
                child.configure(state='disable')
            except:
                pass                                    
        self.imageProgressbar.start()
        self.filterThread.start()
        self.update_idletasks()

    def apply_filters(self):
        startTime = time.time()
        self.tempImage = copy.deepcopy(self.sourceImage)
        self.isImageSaved = False
        for x in self.filterQueue:
            x()
        self.update_preview()
        self.imageProgressbar.stop()
        print('Elapsed Time: ', '{:1.2f}'.format(time.time()-startTime))
        for child in self.bottomConfigFrame.winfo_children():
            try:
                child.configure(state='normal')
            except:
                pass   

    def rand_values(self):
        if(self.rgbOffsetFilterBetterCheckButtonState.get()):
            minPixX = int((self.sourceImage.width/100)*0.5)
            minPixY = int((self.sourceImage.height/100)*0.5)
            self.rgbOffsetFilterRedXvar.set(      random.randint(-minPixX, minPixX))
            self.rgbOffsetFilterRedYvar.set(      random.randint(-minPixY, minPixY))
            self.rgbOffsetFilterGreenXvar.set(    random.randint(-minPixX, minPixX))
            self.rgbOffsetFilterGreenYvar.set(    random.randint(-minPixY, minPixY))
            self.rgbOffsetFilterBlueXvar.set(     random.randint(-minPixX, minPixX))
            self.rgbOffsetFilterBlueYvar.set(     random.randint(-minPixY, minPixY))
            del minPixX, minPixY
        else:
            self.rgbOffsetFilterRedXvar.set(      random.randint(-self.sourceImage.width,     self.sourceImage.width))
            self.rgbOffsetFilterRedYvar.set(      random.randint(-self.sourceImage.height,    self.sourceImage.height))
            self.rgbOffsetFilterGreenXvar.set(    random.randint(-self.sourceImage.width,     self.sourceImage.width))
            self.rgbOffsetFilterGreenYvar.set(    random.randint(-self.sourceImage.height,    self.sourceImage.height))
            self.rgbOffsetFilterBlueXvar.set(     random.randint(-self.sourceImage.width,     self.sourceImage.width))
            self.rgbOffsetFilterBlueYvar.set(     random.randint(-self.sourceImage.height,    self.sourceImage.height))
        
        
        #Big Blocks Offset
        self.bigBlocksFilterBlockCountVar.set(random.randint(1, 8))
        self.bigBlocksFilterBlockMaxHeight.set(int(self.sourceImage.height/self.bigBlocksFilterBlockCountVar.get()))
        self.bigBlocksFilterSeedVar.set(random.randint(0,99999))

        #Small Blocks Filter
        self.smallBlocksFilterSeed.set(random.randint(0,99999))

        #Burn Noise Filter
        self.burnNoiseFilterStretchWidth.set(random.randint(30, 75))
        self.burnNoiseFilterSeed.set(random.randint(0,99999))

        self.apply_changes()

    def preview_fullsized_image(self):
        try:
            self.tempImage.show()
        except:
            glitchLogger.exception('Image preview failed!')
            showerror('Error', 'Image preview failed!\n(Your System must provide an image viewer)')

    def continue_without_save(self):
        if self.isImageSaved:
            return True
        else:
            title   = 'Unsaved Image'
            message = 'There are unsaved changes.\nIf you continue, these changes will be lost.\n\nContinue without saveing?'
            if askyesno(title, message):
                return True
            else:
                return False

    def quit_program(self):
        if self.continue_without_save():
            self.quit()

    #Filters******************************************************************************************************************
    def rgbOffsetFilter(self):
        if self.rgbOffsetFilterActiveState.get():
            print('RGB Offset Filter: started')
            #Create Variables
            sImage = copy.deepcopy(self.tempImage)
            sData = sImage.getdata()
            width, height = sImage.size
            size = width, height

            #Create temporary Images
            gImage = Image.new('RGB', size)

            redImage = Image.new('RGB', size)
            greenImage = Image.new('RGB', size)
            blueImage = Image.new('RGB', size)

            #Split RGB channels 
            r, g, b = sImage.split()        #RGB Channels of the source Image
            rNu, gNu, bNu = gImage.split()  #'RGB' Channels of the generated Image -> all black 

            #Create an Image for every channel (merge colored and black channels)
            redImage = Image.merge('RGB' , (r, gNu, bNu))
            greenImage = Image.merge('RGB' , (rNu, g, bNu))
            blueImage = Image.merge('RGB' , (rNu, gNu, b))
 
            #Offsets every temporary Image by values given from user
            redImage = ImageChops.offset(redImage, self.rgbOffsetFilterRedXvar.get(), self.rgbOffsetFilterRedYvar.get())
            greenImage = ImageChops.offset(greenImage, self.rgbOffsetFilterGreenXvar.get(), self.rgbOffsetFilterGreenYvar.get())
            blueImage = ImageChops.offset(blueImage, self.rgbOffsetFilterBlueXvar.get(), self.rgbOffsetFilterBlueYvar.get())

            #Again splits the RGB channels of the temporary Images
            r, gNu, bNu = redImage.split()
            rNu, g, bNu = greenImage.split()
            rNu, gNu, b = blueImage.split()

            #Merge them to final Image
            gImage = Image.merge('RGB', (r, g, b))
            gImage.load()

            self.tempImage = copy.deepcopy(gImage)
            print('RGB Offset Filter: finished')

    def bigBlocksFilter(self):
        if self.bigBlocksFilterActiveState.get():
            print('Big Blocks Filter: started')
            random.seed(self.bigBlocksFilterSeedVar.get())
            sImage = copy.deepcopy(self.tempImage)
            sImage.load()
            width, height = sImage.size
            size = width, height

            gImage = copy.deepcopy(sImage)

            x = 0
            while(x < self.bigBlocksFilterBlockCountVar.get()):
                #Define height and top edge (and bottom edge) of chunk
                randomHeight = random.randint(int((self.bigBlocksFilterBlockMaxHeight.get()/100)*10), int(self.bigBlocksFilterBlockMaxHeight.get()))
                randYtop = random.randint(x * self.bigBlocksFilterBlockMaxHeight.get(), x * self.bigBlocksFilterBlockMaxHeight.get() + randomHeight)
                randYbottom = randYtop + randomHeight

                #Cut chunk with predefined values
                tempCrop = sImage.crop((0, randYtop, width, randYbottom))

                #Generate random offset value and apply transposed chunk 
                if(random.random() > 0.5):
                    randXoffset = random.randint(0, int((width/100)*self.bigBlocksFilterBlockMaxOffset.get()))
                    gImage.paste(tempCrop, (randXoffset        , randYtop))
                    gImage.paste(tempCrop, (randXoffset - width, randYtop))
                else:
                    randXoffset = -random.randint(0, int((width/100)*self.bigBlocksFilterBlockMaxOffset.get()))
                    gImage.paste(tempCrop, (randXoffset        , randYtop))
                    gImage.paste(tempCrop, (randXoffset + width, randYtop))

                x += 1

            self.tempImage = copy.deepcopy(gImage)
            random.seed()   #Randomize seed
            print('Big Blocks Filter: finished')

    def screenLinesFilter(self):
        if self.screenLinesFilterActiveState.get():
            print('Screen Lines Filter: startetd')
            sImage = copy.deepcopy(self.tempImage)
            sImage.load()
            width, height = sImage.size
            size = width, height

            maskImage       = Image.new('RGB', size, color=(0,0,0))
            draw            = ImageDraw.Draw(maskImage, 'RGB')

            try:    #Catch division by zero
                lineSpacing     = int(100 / self.screenLinesFilterLineDensity.get())
            except:
                lineSpacing     = int(100 / 1)

            try:    #Catch division by zero
                lineCount       = int((height / (self.screenLinesFilterLineThickness.get() + lineSpacing))) +2
            except:
                lineCount       = int((height / 1)) +2

            lineColor       = (self.screenLinesFilterLineColorRed.get(),self.screenLinesFilterLineColorGreen.get(),self.screenLinesFilterLineColorBlue.get())
            lineColorScale  = 1.0

            for x in range(lineCount):
                if self.screenLinesFilterRandomVar.get():
                    lineColorScale = random.uniform(0.7, 1.0)
                    lineColor = (int(self.screenLinesFilterLineColorRed.get() * lineColorScale), int(self.screenLinesFilterLineColorGreen.get() * lineColorScale), int(self.screenLinesFilterLineColorBlue.get() * lineColorScale))
                draw.line(((0,x*(lineSpacing+self.screenLinesFilterLineThickness.get())), (width,x*(lineSpacing+self.screenLinesFilterLineThickness.get()))), fill=lineColor, width=self.screenLinesFilterLineThickness.get())

            del draw
            maskImage   = maskImage.filter(ImageFilter.GaussianBlur(self.screenLinesFilterLineBlur.get()))
            maskImage   = maskImage.convert('RGBA')
            sImage      = sImage.convert('RGBA')

            try:
                maskImage   = np.array(maskImage)   #Convert Pillow Image to numpy array,
                sImage      = np.array(sImage)      # for usage in blend_modes module
                maskImage   = maskImage.astype(float)
                sImage      = sImage.astype(float)

                if self.screenLinesFilterBlendmode.get() == 'Soft Light':
                    sImage = blend_modes.soft_light(sImage, maskImage, 1.0)

                if self.screenLinesFilterBlendmode.get() == 'Lighten Only':
                    sImage = blend_modes.lighten_only(sImage, maskImage, 1.0)

                if self.screenLinesFilterBlendmode.get() == 'Addition':
                    sImage = blend_modes.addition(sImage, maskImage, 1.0)

                if self.screenLinesFilterBlendmode.get() == 'Darken Only':
                    sImage = blend_modes.darken_only(sImage, maskImage, 1.0)

                if self.screenLinesFilterBlendmode.get() == 'Subtract':
                    sImage = blend_modes.subtract(sImage, maskImage, 1.0)

                if self.screenLinesFilterBlendmode.get() == 'Grain Merge':
                    sImage = blend_modes.grain_merge(sImage, maskImage, 1.0)

                if self.screenLinesFilterBlendmode.get() == 'Divide':
                    sImage = blend_modes.divide(sImage, maskImage, 1.0)
            except MemoryError:
                glitchLogger.exception('Memory Error with ScreenFilter!')
                showerror('Memory Error', 'Ran out of Memory!\n\nSolutions:\n - Use 64bit Python\n - Use smaller Images\n - Deactivate "Screen Lines"')

            sImage = np.uint8(sImage)
            sImage = Image.fromarray(sImage)
            sImage = sImage.convert('RGB')

            self.tempImage = copy.deepcopy(sImage)
            print('Screen Lines Filter: finished')
    
    def burnNoiseFilter(self):
        if self.burnNoiseFilterActiveState.get():
            print('Burning Noise Filter: started')
            random.seed(self.burnNoiseFilterSeed.get())
            np.random.seed(self.burnNoiseFilterSeed.get())
            sImage = copy.deepcopy(self.tempImage)
            sImage.load()
            width, height = sImage.size
            size = width, height

            noiseHeight = int((height / self.burnNoiseFilterPixelSize.get()) - (height / self.burnNoiseFilterPixelSize.get()) / 100 * self.burnNoiseFilterStretchHeight.get())
            noiseWidth  = int((width  / self.burnNoiseFilterPixelSize.get()) - (width  / self.burnNoiseFilterPixelSize.get()) / 100 * self.burnNoiseFilterStretchWidth.get())

            if self.burnNoiseFilterColor.get():
                noiseDataOne    = np.random.randint(self.burnNoiseFilterDark.get(), self.burnNoiseFilterBright.get(), (noiseHeight*noiseWidth))
                noiseDataTwo    = np.random.randint(self.burnNoiseFilterDark.get(), self.burnNoiseFilterBright.get(), (noiseHeight*noiseWidth))
                noiseDataThree  = np.random.randint(self.burnNoiseFilterDark.get(), self.burnNoiseFilterBright.get(), (noiseHeight*noiseWidth))
                noiseData       = list(zip(noiseDataOne, noiseDataTwo, noiseDataThree))

                tempNoiseMask   = Image.new('RGB', (noiseWidth, noiseHeight))
                noiseMask       = Image.new('RGB', size)
                tempNoiseMask.putdata(noiseData)

                noiseMask = tempNoiseMask.resize(size, resample=Image.NEAREST)
            else:
                noiseData       = np.random.randint(self.burnNoiseFilterDark.get(), self.burnNoiseFilterBright.get(), (noiseHeight*noiseWidth))

                tempNoiseMask   = Image.new('L', (noiseWidth, noiseHeight))
                noiseMask       = Image.new('L', size)
                tempNoiseMask.putdata(noiseData)

                noiseMask = tempNoiseMask.resize(size, resample=Image.NEAREST)
                noiseMask = noiseMask.convert('RGB')

            burnedImage = copy.deepcopy(sImage)
            tempContrast = float(1-self.burnNoiseFilterContrast.get()/100)

            if tempContrast <= 0.0: 
                tempContrast = 0.001

            if self.burnNoiseFilterInvert.get():
                burnedImage = ImageChops.subtract(noiseMask, burnedImage, tempContrast)
            else:
                burnedImage = ImageChops.subtract(burnedImage, noiseMask, tempContrast)

            if self.burnNoiseFilterBlur.get() != 0:
                burnedImage = burnedImage.filter(ImageFilter.GaussianBlur(self.burnNoiseFilterBlur.get()))

            tempAlpha = float(self.burnNoiseFilterIntensity.get() / 100)

            sImage = ImageChops.blend(sImage, burnedImage, tempAlpha)

            self.tempImage = copy.deepcopy(sImage)

            random.seed()
            np.random.seed()
            del self.randomNoiseData[:]
            print('Burning Noise Filter: finished')

    def rgbScreenFilter(self):
        if self.rgbScreenFilterActiveState.get():
            print('RGB Screen Filter: started')
            sImage = copy.deepcopy(self.tempImage)
            sImage.load()
            width, height = sImage.size
            size = width, height

            pixelSize = self.rgbScreenFilterPixelSize.get()
            pixelGap  = self.rgbScreenFilterPixelGap.get()

            pixelWidth = pixelSize + pixelGap
            columns = int(width/pixelWidth)
            rows = int(height/pixelWidth)

            firstColor  = (self.rgbScreenFilterFirstRed.get(),  self.rgbScreenFilterFirstGreen.get(),   self.rgbScreenFilterFirstBlue.get())
            secondColor = (self.rgbScreenFilterSecondRed.get(), self.rgbScreenFilterSecondGreen.get(),  self.rgbScreenFilterSecondBlue.get())
            thirdColor  = (self.rgbScreenFilterThirdRed.get(),  self.rgbScreenFilterThirdGreen.get(),   self.rgbScreenFilterThirdBlue.get())

            maskImage = Image.new('RGB', size)
            draw = ImageDraw.Draw(maskImage)
            
            #Draw verikal Lines of the black Gap and three Colors on the mask
            for x in range(0,columns+1):
                draw.line((x*pixelWidth,0,x*pixelWidth, height-1), fill='black',width=pixelGap)
                draw.line(( int(pixelSize/3) *0 + pixelGap + x*pixelWidth, 0, int(pixelSize/3) *0 + pixelGap + x*pixelWidth, height-1), fill=firstColor,  width=int(pixelSize/3))
                draw.line(( int(pixelSize/3) *1 + pixelGap + x*pixelWidth, 0, int(pixelSize/3) *1 + pixelGap + x*pixelWidth, height-1), fill=secondColor, width=int(pixelSize/3))
                draw.line(( int(pixelSize/3) *2 + pixelGap + x*pixelWidth, 0, int(pixelSize/3) *2 + pixelGap + x*pixelWidth, height-1), fill=thirdColor,  width=int(pixelSize/3))
            
            #Draw horizontal Lines of the black Gap over the mask
            for x in range(0,rows+1):
                draw.line((0, x*pixelWidth, width, x*pixelWidth), fill='black', width=pixelGap)

            intensity = float(self.rgbScreenFilterIntensity.get()/100)

            tempCopySimage = copy.deepcopy(sImage)
            maskImage = ImageChops.multiply(tempCopySimage, maskImage)
            maskImage = maskImage.filter(ImageFilter.GaussianBlur(self.rgbScreenFilterBlur.get()))
            sImage = ImageChops.blend(sImage, maskImage, intensity)

            self.tempImage = copy.deepcopy(sImage)
            print('RGB Screen Filter: finished')

    def smallBlocksFilter(self):
        if self.smallBlocksFilterActiveState.get():
            print('Small Blocks Filter: started')
            random.seed(self.smallBlocksFilterSeed.get())
            np.random.seed(self.smallBlocksFilterSeed.get())
            sImage = copy.deepcopy(self.tempImage)
            sImage.load()
            width, height = sImage.size
            size = width, height

            x = 0
            while(x < self.smallBlocksFilterBlocksCount.get()):
                #Define height, width and all edges of chunk
                randomHeight    = random.randint(self.smallBlocksFilterMinHeight.get(), self.smallBlocksFilterMaxHeight.get())
                randomWidth     = random.randint(self.smallBlocksFilterMinWidth.get(), self.smallBlocksFilterMaxWidth.get())
                randYtop        = random.randint(0, height-10)
                randYbottom     = randYtop + randomHeight
                randXleft       = random.randint(-randomWidth, width + randomWidth)
                if randXleft < 0:
                    randXleft = randXleft - randXleft
                randXright      = randXleft + randomWidth
                if randXright >= width:
                    randXleft  = width - randomWidth
                    randXright = width

                crop = (randXleft, randYtop, randXright, randYbottom)

                #Cut chunk with predefined values
                tempCrop = sImage.crop(crop)

                r, g, b = tempCrop.split()        #RGB Channels of the source Image
                tempCrop = Image.new('RGB', tempCrop.size, color=(0,0,0))
                rNu, gNu, bNu = tempCrop.split()  #'RGB' Channels of the generated Image -> all black 
                
                #Randomly paste Chunk with given colors
                rand = random.random()
                if rand < 0.3:
                    redImage = Image.merge('RGB' , (r, g, bNu))
                    sImage.paste(redImage, crop)
                elif 0.3 <= rand < 0.6:
                    greenImage = Image.merge('RGB' , (rNu, g, b))
                    sImage.paste(greenImage, crop)
                else:
                    blueImage = Image.merge('RGB' , (r, gNu, b))
                    sImage.paste(blueImage, crop)

                x += 1

            self.tempImage = copy.deepcopy(sImage)

            random.seed()
            np.random.seed()
            print('Small Blocks Filter: finished')

    def barrelFilter(self):
        z=0
        #if self.barrelFilterActiveState.get():
        if z:
            print('Barrel Filter: started')
            sImage = copy.deepcopy(self.tempImage)
            sImage.load()
            width, height = sImage.size
            size = width, height
            
            #Implement Algorithm - not implemented yet

            self.tempImage = copy.deepcopy(sImage)

            del sImage, width, height, size
            print('Barrel Filter: finished')

    def testFilter(self):
        z=0
        #if self.nameFilterActiveState.get():
        if z:
            print('Test Filter: started')
            sImage = copy.deepcopy(self.tempImage)
            sImage.load()
            width, height = sImage.size
            size = width, height
            
            gImage = copy.deepcopy(sImage)

            #Implement Algorithm

            self.tempImage = copy.deepcopy(sImage)
            print('Test Filter: finished')

    #Filter Functions*********************************************************************************************************
    def rgbOffset_rand_values(self):
        #RGB Offset
        if(self.rgbOffsetFilterBetterCheckButtonState.get()):
            minPixX = int((self.sourceImage.width/100)*0.3)
            minPixY = int((self.sourceImage.height/100)*0.3)
            self.rgbOffsetFilterRedXvar.set(      random.randint(-minPixX, minPixX))
            self.rgbOffsetFilterRedYvar.set(      random.randint(-minPixY, minPixY))
            self.rgbOffsetFilterGreenXvar.set(    random.randint(-minPixX, minPixX))
            self.rgbOffsetFilterGreenYvar.set(    random.randint(-minPixY, minPixY))
            self.rgbOffsetFilterBlueXvar.set(     random.randint(-minPixX, minPixX))
            self.rgbOffsetFilterBlueYvar.set(     random.randint(-minPixY, minPixY))
            del minPixX, minPixY
        else:
            self.rgbOffsetFilterRedXvar.set(      random.randint(-self.sourceImage.width,     self.sourceImage.width))
            self.rgbOffsetFilterRedYvar.set(      random.randint(-self.sourceImage.height,    self.sourceImage.height))
            self.rgbOffsetFilterGreenXvar.set(    random.randint(-self.sourceImage.width,     self.sourceImage.width))
            self.rgbOffsetFilterGreenYvar.set(    random.randint(-self.sourceImage.height,    self.sourceImage.height))
            self.rgbOffsetFilterBlueXvar.set(     random.randint(-self.sourceImage.width,     self.sourceImage.width))
            self.rgbOffsetFilterBlueYvar.set(     random.randint(-self.sourceImage.height,    self.sourceImage.height))
    
    #Windows******************************************************************************************************************
    def open_filterList_window(self):
        if not self.filterListOpen:
            self.filterListOpen = True
            filterListWindow(self)

    def open_presetList_window(self):
        if not self.presetListOpen:
            self.presetListOpen = True
            presetListWindow(self)

    def open_about_window(self):
        if not self.aboutWindowOpen:
            self.aboutWindowOpen = True
            aboutWindow(self)


class filterListWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.geometry('+900+120')
        self.title('Filter List')
        try:
            self.iconbitmap('GlitchFilterIcon.ico')
        except:
            glitchLogger.warning("Icon couldn't be loaded - filter list window")
        self.resizable(False, False)
        self.transient(master)
        self.protocol('WM_DELETE_WINDOW', self.hideWindow)

        #Define Widgets
        self.filterListFrame                = tk.LabelFrame(self, text='Active Filter')

        self.rgbOffsetFilterCheckBox        = tk.Checkbutton(self.filterListFrame, text='RGB Offset', selectcolor='gray30', variable=master.rgbOffsetFilterActiveState, command=master.refresh_filter)
        self.bigBlocksFilterCheckBox        = tk.Checkbutton(self.filterListFrame, text='Big Blocks Offset', selectcolor='gray30', variable=master.bigBlocksFilterActiveState, command=master.refresh_filter)
        self.smallBlocksFilterCheckBox      = tk.Checkbutton(self.filterListFrame, text='Small Blocks Offset', selectcolor='gray30', variable=master.smallBlocksFilterActiveState, command=master.refresh_filter)
        self.burnNoiseFilterCheckBox        = tk.Checkbutton(self.filterListFrame, text='Burning Noise', selectcolor='gray30', variable=master.burnNoiseFilterActiveState, command=master.refresh_filter)
        self.rgbScreenFilterCheckBox        = tk.Checkbutton(self.filterListFrame, text='RGB Screen', selectcolor='gray30', variable=master.rgbScreenFilterActiveState, command=master.refresh_filter)
        self.screenLinesFilterCheckBox      = tk.Checkbutton(self.filterListFrame, text='Screen Lines', selectcolor='gray30', variable=master.screenLinesFilterActiveState, command=master.refresh_filter)

        #Display Widgets
        self.filterListFrame.grid(              column=0, row=0, sticky=tk.NW)

        self.rgbOffsetFilterCheckBox.grid(      column=0, row=0, sticky=tk.NW)
        self.bigBlocksFilterCheckBox.grid(      column=0, row=1, sticky=tk.NW)
        self.smallBlocksFilterCheckBox.grid(    column=0, row=2, sticky=tk.NW)
        self.burnNoiseFilterCheckBox.grid(      column=0, row=3, sticky=tk.NW)
        self.rgbScreenFilterCheckBox.grid(      column=0, row=4, sticky=tk.NW)
        self.screenLinesFilterCheckBox.grid(    column=0, row=5, sticky=tk.NW)

    def hideWindow(self):
        self.withdraw()
        self.master.filterListOpen = False

class presetListWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.geometry('+950+150')
        self.title('Presets')
        try:
            self.iconbitmap('GlitchFilterIcon.ico')
        except:
            glitchLogger.warning("Icon couldn't be loaded - preset list window")
        self.resizable(False, False)
        self.transient(master)
        self.protocol('WM_DELETE_WINDOW', self.hideWindow)

        self.create_widgets()

    def create_widgets(self):
        self.presetListbox      = tk.Listbox(self)
        self.presetNameEntry    = tk.Entry(self)
        self.presetButton       = tk.Button(self,text='test', command=self.save_new_preset)

        self.presetListbox.grid(    column=0, row=0, padx=2, pady=2)
        self.presetNameEntry.grid(  column=0, row=1, padx=2, pady=2)
        self.presetButton.grid(     column=0, row=2, padx=2, pady=2)

    def save_new_preset(self):  #DOES NOT WORK YET!
        fileName = self.presetNameEntry.get(), '.csv'
        print(fileName)
        for i in range(len(self.master.variableList)):
            print(self.master.variableList[i])
        with open(fileName, 'w') as out_file:
            for i in range(len(self.master.variableList)):
                print(self.master.variableList[i])

    def hideWindow(self):
        self.master.presetListOpen = False
        self.withdraw()

class aboutWindow(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.resizable(False, False)
        self.transient(master)
        self.geometry('+250+250')
        self.title('About Glitch Filter')
        try:
            self.master.iconbitmap('GlitchFilterIcon.ico')
        except:
            glitchLogger.warning("Icon couldn't be loaded - about window")
        self.protocol('WM_DELETE_WINDOW', self.destroyWindow)
        
        text = ' Glitch Filter\n by stubbornGarrett\n\n Built:\t5th May 2019 \n Version:\t1.0\n Python:\t3.7 '

        self.textFrame = tk.Frame(self)
        self.textLabel = tk.Label(self.textFrame, text=text, justify=tk.LEFT, bg='#aa00aa', fg='cyan', font=('Tahoma', 11, 'bold'))
        self.textFrame.pack()
        self.textLabel.pack()#padx=10, pady=10)
    
    def destroyWindow(self):
        self.master.aboutWindowOpen = False
        self.withdraw()

class CreateToolTip(object):
    """ tk_ToolTip_class101.py
    gives a Tkinter widget a tooltip as the mouse is above the widget
    tested with Python27 and Python34  by  vegaseat  09sep2014
    www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter

    Modified to include a delay time by Victor Zaccardo, 25mar16
    """
    
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 130   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="gray40", relief='solid', borderwidth=1,
                       wraplength = self.wraplength, font=('Tahoma', 8))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


def main():
    try:
        root = tk.Tk()

        root.option_add('*Font', ('Tahoma', 11))
        root.option_add('*Label.width', '18')
        root.option_add('*Label.width', '20')
        root.option_add('*Label.background', thiColor)
        root.option_add('*Spinbox.width', '5')
        root.option_add('*Listbox.background', secColor)
        root.option_add('*Button.background', secColor)
        root.option_add('*Spinbox.background', secColor)
        root.option_add('*Scale.background', secColor)
        root.option_add('*Scale.troughcolor', secColor)

        application = Application(root)
    except Exception:
        glitchLogger.critical('Initalisation of window failed!')
    else:
        application.mainloop()

if __name__ == '__main__':
    main()