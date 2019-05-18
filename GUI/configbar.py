from tools import logger
import tkinter as tk
import tkinter.ttk as ttk
#from filter import rgboffset

class Configbar(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)#, width=400)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.bind('<Configure>', self.min_max_size)

        self.init_widgets()

    def init_widgets(self):
        self.topConfigFrame     = ttk.Frame(self)
        self.topConfigFrame.grid(       column=0, row=0, sticky=tk.W+tk.E)
        self.topConfigFrame.columnconfigure( 0, weight=1)
        self.topCanvas          = tk.Canvas(self.topConfigFrame, bg='green')
        self.topCanvas.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

        self.firstSeperator     = ttk.Separator(self)
        self.firstSeperator.grid(       column=0, row=1, sticky=tk.W+tk.E)

        self.filterConfigFrame  = ttk.Frame(self)
        self.filterConfigFrame.grid(    column=0, row=2, sticky=tk.W+tk.E+tk.N+tk.S)
        self.filterConfigFrame.columnconfigure( 0, weight=1)
        self.filterConfigFrame.rowconfigure(    0, weight=1)
        self.imageCanvas        = tk.Canvas(self.filterConfigFrame, bg='blue')
        self.imageCanvas.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

        self.secondSeperator    = ttk.Separator(self)
        self.secondSeperator.grid(      column=0, row=3, sticky=tk.W+tk.E)

        self.bottomConfigFrame  = ttk.Frame(self)
        self.bottomConfigFrame.grid(    column=0, row=4, sticky=tk.W+tk.E)
        self.bottomConfigFrame.columnconfigure( 0, weight=1)

        self.applyButton        = ttk.Button(self.bottomConfigFrame, text='Apply Changes').grid(column=0, row=1, sticky=tk.W+tk.E) #, command=rgboffset.rgbOffsetFilter

        #rgboffset.create_parameters(self)
        #rgboffset.create_widgets(self, self)

    def min_max_size(self, event):
        if self.winfo_width() > 400:
            self.config(width=400)
        elif self.winfo_width() < 200:
            self.config(width=200)
        else:
            pass
