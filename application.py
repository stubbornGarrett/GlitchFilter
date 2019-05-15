from GUI.menubar import Menubar
#from GUI.toolbar
from GUI.imagepreview import Imagepreview
from GUI.configbar import Configbar
from tools import logger
import tkinter as tk
import tkinter.ttk as ttk

class GlitchFilter(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.master.geometry('800x500+50+50')
        self.master.title('Glitch Filter')
        self.master.protocol('WM_DELETE_WINDOW', self.quit_application)
        self.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

        self.init_gui(self)

    def init_gui(self, parent):
        tk.Grid.columnconfigure(parent, 0, weight=1)
        tk.Grid.rowconfigure(parent, 0, weight=1)
        Menubar(parent.master, parent)
        Imagepreview(parent)
        Configbar(parent)

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