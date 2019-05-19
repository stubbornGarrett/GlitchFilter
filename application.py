from tools import logger, styleconfig
from GUI.menubar import Menubar
#from GUI.toolbar
from GUI.imagepreview import Imagepreview
from GUI.configbar import Configbar
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.ttk as ttk
import copy

class GlitchFilter(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.master.geometry('800x500+50+50')
        self.master.title('Glitch Filter')
        self.master.protocol('WM_DELETE_WINDOW', self.quit_application)
        self.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)
        try:
            self.master.iconbitmap('GlitchFilterIcon.ico')
        except:
            logger.log.warning("Icon couldn't be loaded - main window")

        self.GlitchStyle = styleconfig.GlitchStyle()

        self.sourceImage             = Image.new('RGB', (1,1), 'pink')
        self.sourceImagePath         = ''
        self.sourceImageExtension    = '.png'
        self.sourceImageThumbnail    = copy.copy(self.sourceImage)
        self.tempImageThumbnail      = copy.copy(self.sourceImage)
        self.tempImage               = copy.copy(self.sourceImage)

        self.firstImageLoaded        = False
        
        self.previewActiveVar        = tk.IntVar()
        self.previewActiveVar.set(1)
        self.highResActiveVar        = tk.IntVar()
        self.highResActiveVar.set(0)
        
        self.filterListStr = []
        self.filterListVar           = tk.StringVar()

        self.FILEOPTIONS =  dict(   filetypes=[\
                                ('JPEG','*.jpg *.jpeg'),
                                ('PNG','*.png'),
                                ("all files","*.*")])

        self.sizeMultiplicator  = 1.0
        self.previewXoffset     = 0
        self.previewYoffset     = 0


        self.init_gui()
        self.set_binds()

    def init_gui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.menubar = Menubar(self.master, self)
        self.panedMainWindow    = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panedMainWindow.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.panedMainWindow.rowconfigure(0, weight=1)

        self.imagepreviewWidget = Imagepreview(self.panedMainWindow)
        self.configbarWidget    = Configbar(self.panedMainWindow)

        self.panedMainWindow.add(self.imagepreviewWidget, weight=10)
        self.panedMainWindow.add(self.configbarWidget, weight=1)

    def set_binds(self):
        self.master.bind('<Control-a>', self.configbarWidget.apply_filter)
        self.master.bind('<Control-r>', self.configbarWidget.apply_filter_random)
        self.master.bind('<Control-f>', self.configbarWidget.preview_image)
        
        self.master.bind('<Control-x>', self.reset_preview_values)
        
        self.master.bind('<Left>',         self.imagepreviewWidget.update_preview_offset)
        self.master.bind('<Right>',        self.imagepreviewWidget.update_preview_offset)
        self.master.bind('<Up>',           self.imagepreviewWidget.update_preview_offset)
        self.master.bind('<Down>',         self.imagepreviewWidget.update_preview_offset)

    def reset_preview_values(self, event=None):
        self.sizeMultiplicator   = 1.0
        self.previewXoffset      = 0
        self.previewYoffset      = 0
        self.imagepreviewWidget.adjust_canvas_size()

    def quit_application(self):
        self.quit()

def main():
    try:
        root = tk.Tk()
        tk.Grid.columnconfigure(root, 0, weight=1)
        tk.Grid.rowconfigure(root, 0, weight=1)
        application = GlitchFilter(root)
        root.update()
        root.minsize(root.winfo_width(), root.winfo_height())
        root.state('zoomed')
        #root.update_idletasks
    except Exception:
        logger.log.exception('Initalisation of window failed!')
    else:
        application.update()
        application.imagepreviewWidget.previewCanvas.config(width=application.imagepreviewWidget.winfo_width(), height=application.imagepreviewWidget.winfo_height())
        application.mainloop()

if __name__ == '__main__':
    main()