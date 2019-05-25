from tools import logger, styleconfig
import configparser
import os.path
from configparser import ConfigParser
from copy import copy
from GUI.menubar import Menubar
#from GUI.toolbar
from GUI.imagepreview import Imagepreview
from GUI.configbar import Configbar
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk

class GlitchFilter(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        if not os.path.isfile('./settings.ini'):
            self.create_config()
        self.read_config('./settings.ini')

        self.defaultFontSize = 11
        self.create_and_apply_theme()

        self.master.geometry('{}x{}+{}+{}'.format(self.config.get('MainWindow', 'minWidth'), self.config.get('MainWindow', 'minHeight'), self.config.get('MainWindow', 'xStartPos'), self.config.get('MainWindow', 'yStartPos')))
        self.master.title('Glitch Filter')
        self.master.protocol('WM_DELETE_WINDOW', self.quit_application)
        self.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)
        try:
            self.master.iconbitmap('GlitchFilterIcon.ico')
        except:
            logger.log.warning("Icon couldn't be loaded - main window")

        self.create_variables()
        self.init_gui()
        self.set_binds()

    def create_config(self):
        writeConfig = ConfigParser()
        writeConfig.optionxform = str

        writeConfig['MainWindow'] = {
            'minWidth': '800',
            'minHeight': '500',
            'xStartPos': '50',
            'yStartPos': '50',
        }

        writeConfig['Style'] = {
            'backgroundColor': '#212121',
            'lightBackgroundColor': '#424242',
            'fontColor': '#E0E0E0',
            'highlightsColor': '#4DD0E1',
            'darkHighlightsColor': '#E040FB',
            'disableColor': '#757575',
            'disableFontColor': '#9E9E9E',

            'defaultFont': '"Calibri"',
            'defaultFontSize':  '12'
        }

        with open('./settings.ini', 'w') as file:
            writeConfig.write(file)

    def read_config(self, file):
        self.config = configparser.ConfigParser()
        self.config.read('./settings.ini')

    def create_and_apply_theme(self):
        self.backgroundColor  = self.config.get('Style', 'backgroundColor')    #Background
        self.lightBackgroundColor  = self.config.get('Style', 'lightBackgroundColor')    #Background
        self.fontColor        = self.config.get('Style', 'fontColor')          #Font
        self.highlightsColor  = self.config.get('Style', 'highlightsColor')    #Highlights (e.g. hovering a button)
        self.darkHighlightsColor= self.config.get('Style', 'darkHighlightsColor')    #Highlights (e.g. hovering a button)
        self.disableColor     = self.config.get('Style', 'disableColor')
        self.disableFontColor = self.config.get('Style', 'disableFontColor')
        self.defaultFont      = self.config.get('Style', 'defaultFont')
        self.defaultFontSize  = self.config.getint('Style', 'defaultFontSize')
        
        font = '({},{})'.format(self.defaultFont, self.defaultFontSize)

        self.style = styleconfig.GlitchStyle()
        self.style.create_theme('GlitchTheme', self.backgroundColor, self.lightBackgroundColor, self.fontColor, self.highlightsColor, self.darkHighlightsColor, self.disableColor, self.disableFontColor, font)
        self.style.theme_use('GlitchTheme')

    def create_variables(self):
        self.sourceImage            = Image.new('RGB', (1,1), 'pink')
        self.sourceImagePath        = ''
        self.sourceImageName        = ''
        self.sourceImageExtension   = '.png'
        self.previewImage           = copy(self.sourceImage)
       # self.tempImageThumbnail      = copy(self.sourceImage)
        self.tempImage              = copy(self.sourceImage)

        self.filetypes              = [ ('JPEG','*.jpg *.jpeg'),
                                        ('PNG','*.png'),
                                        ("all files","*.*")]

        self.firstImageLoaded        = False

        self.previewActiveVar        = tk.IntVar()
        self.previewActiveVar.set(1)
        self.highResActiveVar        = tk.IntVar()
        self.highResActiveVar.set(0)
        
        self.filterListStr  = []
        self.filterListVar           = tk.StringVar()

    def init_gui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.menubar = Menubar(self.master, self)

        self.panedMainWindow    = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panedMainWindow.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.panedMainWindow.rowconfigure(0, weight=1)

        self.imagepreviewWidget = Imagepreview( self.panedMainWindow,   self)
        self.configbarWidget    = Configbar(    self.panedMainWindow,   self)

        self.panedMainWindow.add(self.imagepreviewWidget,   weight=10)
        self.panedMainWindow.add(self.configbarWidget,      weight=1)

    def set_binds(self):
        self.master.bind('<Control-a>', self.configbarWidget.apply_filter)
        self.master.bind('<Control-r>', self.configbarWidget.apply_filter_random)
        self.master.bind('<Control-f>', self.configbarWidget.preview_image)
        
        self.master.bind('<Control-x>', self.imagepreviewWidget.reset_preview_values)

        self.master.bind('<MouseWheel>', self.mouseWheel_events)

    def mouseWheel_events(self, event):
        mouseXpos = self.master.winfo_pointerx()-self.master.winfo_rootx()
        mouseYpos = self.master.winfo_pointery()-self.master.winfo_rooty()

        if mouseXpos >= self.master.winfo_width() - self.configbarWidget.configbarNotebook.winfo_width() and \
           mouseYpos >= self.menubar.winfo_height() + (self.configbarWidget.topConfigFrame.winfo_height() + self.defaultFontSize) +30 and \
           mouseXpos < self.master.winfo_width() and \
           mouseYpos < self.master.winfo_height() - self.configbarWidget.bottomConfigFrame.winfo_height():
            self.configbarWidget.filterConfigCanvas.yview_scroll(int(-1*(event.delta/120)), 'units')
            
    def quit_application(self):
        self.quit()

def main():
    try:
        root = tk.Tk()        
        tk.Grid.columnconfigure(root, 0, weight=1)
        tk.Grid.rowconfigure(root, 0, weight=1)
        application = GlitchFilter(root)
        root.minsize(root.winfo_width(), root.winfo_height())
        root.state('zoomed')
    except Exception:
        logger.log.exception('Initalisation of window failed!')
    else:
        application.mainloop()

if __name__ == '__main__':
    main()