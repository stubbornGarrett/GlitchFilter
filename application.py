from tools import logger, styleconfig
import configparser
import os.path
from configparser import ConfigParser
from copy import copy
from GUI.menubar import Menubar
from GUI.infobar import Infobar
from GUI.imagepreview import Imagepreview
from GUI.configbar import Configbar
from PIL import Image, ImageTk
from tkinter.messagebox import askyesno
import tkinter as tk
import tkinter.ttk as ttk

class GlitchFilter(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)

        if not os.path.isfile('./settings.ini'):
            self.create_config()
        self.read_config('./settings.ini')

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
        self.backgroundColor        = self.config.get('Style', 'backgroundColor')       #Background
        self.lightBackgroundColor   = self.config.get('Style', 'lightBackgroundColor')  #Background
        self.fontColor              = self.config.get('Style', 'fontColor')             #Font
        self.highlightsColor        = self.config.get('Style', 'highlightsColor')       #Highlights (e.g. marking text)
        self.darkHighlightsColor    = self.config.get('Style', 'darkHighlightsColor')   #Highlights (e.g. hovering a button)
        self.disableColor           = self.config.get('Style', 'disableColor')
        self.disableFontColor       = self.config.get('Style', 'disableFontColor')
        self.defaultFont            = self.config.get('Style', 'defaultFont')
        self.defaultFontSize        = self.config.getint('Style', 'defaultFontSize')
        
        font = '({},{})'.format(self.defaultFont, self.defaultFontSize)

        self.style = styleconfig.GlitchStyle()
        self.style.create_theme('GlitchTheme', self.backgroundColor, self.lightBackgroundColor, self.fontColor, self.highlightsColor, self.darkHighlightsColor, self.disableColor, self.disableFontColor, font)
        self.style.theme_use('GlitchTheme')

    def create_variables(self):
        self.sourceImage            = Image.new('RGB', (1,1), 'pink')
        self.sourceImagePath        = ''
        self.sourceImageName        = ''
        self.sourceImageExtension   = '.png'
        self.tempImage              = copy(self.sourceImage)

        self.filetypes              = [ ('JPEG','*.jpg *.jpeg'),
                                        ('PNG','*.png'),
                                        ("all files","*.*")]

        self.imageIsLoaded          = False
        self.imageIsSaved           = True

        self.previewActiveVar       = tk.IntVar()
        self.previewActiveVar.set(1)
        self.highResActiveVar       = tk.IntVar()
        self.highResActiveVar.set(0)

        self.filterListStr  = []
        self.filterListVar          = tk.StringVar()

    def init_gui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.menubar = Menubar(self.master, self)

        self.panedMainWindow    = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panedMainWindow.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.panedMainWindow.rowconfigure(0, weight=1)

        self.leftMainFrame      = ttk.Frame(self.panedMainWindow)
        self.leftMainFrame.columnconfigure(0, weight=1)
        self.leftMainFrame.rowconfigure(0, weight=1)
        self.leftMainFrame.rowconfigure(1, weight=0)
        self.rightMainFrame     = ttk.Frame(self.panedMainWindow)
        self.rightMainFrame.columnconfigure(0, weight=1)
        self.rightMainFrame.rowconfigure(0, weight=1)
        self.panedMainWindow.add(self.leftMainFrame,    weight=4)
        self.panedMainWindow.add(self.rightMainFrame,   weight=1)

        self.imagepreviewWidget = Imagepreview( self.leftMainFrame, backgroundcolor=self.backgroundColor, quality=2)
        self.imagepreviewWidget.grid(           column=0, row=0, sticky='news')
        self.configbarWidget    = Configbar(    self.rightMainFrame,   self)
        self.configbarWidget.grid(              column=0, row=0, sticky='news')

        self.infobarWidget      = Infobar(      self.leftMainFrame)
        self.infobarWidget.grid(                column=0, row=1, sticky='we')

    def set_binds(self):
        def original_zoom(event):
            self.imagepreviewWidget.original_zoom()
            self.infobarWidget.update_previewInfo('x{}'.format(round(self.imagepreviewWidget.canvasScale,2)))
        self.master.bind('1',           original_zoom)
        self.master.bind('<Control-a>', self.configbarWidget.apply_filter)
        self.master.bind('<Control-r>', self.configbarWidget.apply_filter_random)
        self.master.bind('<Control-g>', self.configbarWidget.create_gif)
        self.master.bind('<Control-z>', self.reset_preview)
        self.master.bind('<MouseWheel>',self.mouseWheel_events)

        self.leftMainFrame.bind('<Configure>', self.imagepreviewWidget.adjust_canvas_size)

        def canvas_zoom(event):
            self.imagepreviewWidget.zoom(event)
            self.infobarWidget.update_previewInfo('x{}'.format(round(self.imagepreviewWidget.canvasScale,2)))
        self.imagepreviewWidget.previewCanvas.bind('<MouseWheel>', canvas_zoom)

    def reset_preview(self, event):
        self.imagepreviewWidget.reset_preview()
        self.infobarWidget.update_previewInfo('x{}'.format(round(self.imagepreviewWidget.canvasScale,2)))

    def mouseWheel_events(self, event):
        mouseXpos = self.master.winfo_pointerx()-self.master.winfo_rootx()
        mouseYpos = self.master.winfo_pointery()-self.master.winfo_rooty()

        if mouseXpos >= self.master.winfo_width() - self.configbarWidget.configbarNotebook.winfo_width() and \
           mouseYpos >= self.menubar.winfo_height() + (self.configbarWidget.topConfigFrame.winfo_height() + self.defaultFontSize) +30 and \
           mouseXpos < self.master.winfo_width() and \
           mouseYpos < self.master.winfo_height() - self.configbarWidget.bottomConfigFrame.winfo_height():
            self.configbarWidget.filterConfigCanvas.yview_scroll(int(-1*(event.delta/120)), 'units')

    def continue_without_save(self):
        if not self.imageIsSaved:
            title   = 'Unsaved Image'
            message = 'There are unsaved changes.\nIf you continue, these changes will be lost.\n\nContinue without saveing?'
            return askyesno(title, message)
        else:
            return True

    def update_preview(self):
        if self.previewActiveVar.get():
            self.imagepreviewWidget.scaleChanged = True
            self.imagepreviewWidget.update_image(self.tempImage)
        else:
            self.imagepreviewWidget.scaleChanged = True
            self.imagepreviewWidget.update_image(self.sourceImage)

    def quit_application(self):
        if self.continue_without_save():
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