from GUI.menubar import Menubar
#from GUI.toolbar
from GUI.imagepreview import Imagepreview
from GUI.configbar import Configbar
from tools import logger
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

        self.sourceImage            = Image.new('RGB', (1,1), 'pink')
        self.sourceImagePath        = ''
        self.sourceImageExtension   = '.png'
        self.tempImage              = copy.copy(self.sourceImage)

        self.firstImageLoaded = False

        self.FILEOPTIONS =  dict(   filetypes=[\
                                    ('JPEG','*.jpg *.jpeg'),
                                    ('PNG','*.png'),
                                    ("all files","*.*")])

        self.init_gui(self)
        
        self.master.bind('<Enter>', func=self.imagepreviewWidget.adjust_canvas_size)

    def init_gui(self, parent):
        tk.Grid.columnconfigure(parent, 0, weight=1)
        tk.Grid.rowconfigure(parent, 0, weight=1)
        self.menubarWidget = Menubar(parent.master, parent)
        self.imagepreviewWidget = Imagepreview(parent)
        self.imagepreviewWidget.grid(               column=0, row=0, sticky='news')
        self.imagepreviewWidget.columnconfigure(    0, weight=1)
        self.imagepreviewWidget.rowconfigure(       0, weight=1)
        self.configbarWidget = Configbar(parent)
        self.configbarWidget.grid(                  column=1, row=0, sticky='ns')
        self.configbarWidget.rowconfigure(          0, weight=1)

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
        root.update_idletasks
    except Exception:
        logger.log.exception('Initalisation of window failed!')
    else:
        application.mainloop()

if __name__ == '__main__':
    main()