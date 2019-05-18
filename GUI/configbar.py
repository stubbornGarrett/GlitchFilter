from tools import logger
import tkinter as tk
import tkinter.ttk as ttk
from Filters import rgboffset
from copy import copy

class Configbar(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)#, width=400)
        self.rowconfigure(1, pad=10)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, pad=10)
        self.rowconfigure(4, pad=10)
        self.columnconfigure(0, weight=1)

        self.inProgress = False

        self.filterListObj = []
        self.init_widgets()

    def init_widgets(self):
        self.topConfigFrame     = ttk.Frame(self)
        self.topConfigFrame.grid(       column=0, row=0, sticky=tk.W+tk.E)
        self.topConfigFrame.columnconfigure( 0, weight=1)
        self.topCanvas          = tk.Canvas(self.topConfigFrame, bg='green', height=100)
        self.topCanvas.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)

        self.firstSeperator     = ttk.Separator(self)
        self.firstSeperator.grid(       column=0, row=1, sticky=tk.W+tk.E)

        self.filterConfigFrame  = ttk.Frame(self)
        self.filterConfigFrame.grid(    column=0, row=2, sticky=tk.W+tk.E+tk.N+tk.S)
        self.filterConfigFrame.columnconfigure( 0, weight=1)
        self.filterConfigFrame.rowconfigure(    0, weight=1)

        self.secondSeperator    = ttk.Separator(self)
        self.secondSeperator.grid(      column=0, row=3, sticky=tk.W+tk.E)

        self.bottomConfigFrame  = ttk.Frame(self)
        self.bottomConfigFrame.grid(    column=0, row=4, sticky=tk.W+tk.E)
        self.bottomConfigFrame.columnconfigure( 0, weight=1)
        self.bottomConfigFrame.columnconfigure( 1, weight=1)
        self.bottomConfigFrame.rowconfigure(    0, weight=1, pad=5)
        self.bottomConfigFrame.rowconfigure(    1, weight=1, pad=5)

        self.applyButton        = ttk.Button(self.bottomConfigFrame, text='Apply Changes',              underline=0, command=self.apply_filter).grid(       column=0, row=0, sticky=tk.W+tk.E, padx=5)
        self.randomButton       = ttk.Button(self.bottomConfigFrame, text='Random Render',              underline=0, command=self.apply_filter_random).grid(column=1, row=0, sticky=tk.W+tk.E, padx=5)
        self.showRenderButton   = ttk.Button(self.bottomConfigFrame, text='Preview full sized Image',   underline=8, command=self.preview_image).grid(      column=0, row=1, sticky=tk.W+tk.E, padx=5, columnspan=2)

        self.rgboffsetFilter = rgboffset.RGBoffsetFilter(self.filterConfigFrame, self)
        self.filterListObj.append(self.rgboffsetFilter)
        self.rgboffsetFilter.display_widgets()

    def apply_filter_random(self, event=None):
        self.disable_configbar()
        image = self.master.master.sourceImage
        for filter in self.filterListObj:
            filter.random_values()
            image = filter.applyFilter(image)
        self.master.master.tempImage = copy(image)
        self.master.master.tempImageThumbnail = self.master.master.menubar.create_thumbnail(self.master.master.tempImage)
        self.master.master.imagepreviewWidget.display_image(self.master.master.tempImageThumbnail)
        self.enable_configbar()

    def apply_filter(self, event=None):
        self.disable_configbar()
        image = self.master.master.sourceImage
        for filter in self.filterListObj:
            image = filter.applyFilter(image)
        self.master.master.tempImage = copy(image)
        self.master.master.tempImageThumbnail = self.master.master.menubar.create_thumbnail(self.master.master.tempImage)
        self.master.master.imagepreviewWidget.display_image(self.master.master.tempImageThumbnail)
        self.enable_configbar()
        
    def preview_image(self, event=None):
        self.master.master.tempImage.show()

    def disable_configbar(self, state='disabled'):
        self.inProgress = True
        def changeState(widget):
            if widget.winfo_children:
                for child in widget.winfo_children():
                    try:
                        child.configure(state=state)
                    except:
                        pass
                    changeState(child)
        changeState(self.filterConfigFrame)
        changeState(self.bottomConfigFrame)
        self.master.master.master.update_idletasks()

    def enable_configbar(self):
        self.disable_configbar('!disabled')

#    def enable_configbar(self):
#        for child in self.winfo_children():
#            child.configure(state='normal')
#        self.inProgress = False