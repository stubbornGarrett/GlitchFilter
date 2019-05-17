from tools import logger, globals
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

        self.init_gui()

    def init_gui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.menubar = Menubar(self.master, self)
        self.panedMainWindow    = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panedMainWindow.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)
        self.panedMainWindow.rowconfigure(0, weight=1)

        self.imagepreviewWidget = Imagepreview(self.panedMainWindow)
        self.configbarWidget    = Configbar(self.panedMainWindow)

        self.panedMainWindow.add(self.imagepreviewWidget, weight=20)
        self.panedMainWindow.add(self.configbarWidget, weight=1)

        #self.panedMainWindow.rowconfigure(0, weight=1)
        self.master.bind('<Enter>', lambda event: self.imagepreviewWidget.adjust_canvas_size(event, image=globals.sourceImageThumbnail))

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