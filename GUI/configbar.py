from tools import logger
import tkinter as tk
import tkinter.ttk as ttk
from Filters import rgboffset
from copy import copy

class Configbar(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)#, width=400)
        #self.rowconfigure(1, pad=10)
        #self.rowconfigure(2, weight=1)
        #self.rowconfigure(3, pad=10)
        #self.rowconfigure(4, pad=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.inProgress = False

        self.filterListObj = []
        self.init_widgets()

    def init_widgets(self):
        self.configbarNotebook = ttk.Notebook(self)
        self.configbarNotebook.grid(column=0, row=0, sticky='news')

        #Confgig Tab ****************************************************************************
        self.configTab          = ttk.Frame(self.configbarNotebook)
        
        self.configTab.rowconfigure(1, pad=10)
        self.configTab.rowconfigure(2, weight=1)
        self.configTab.rowconfigure(3, pad=10)
        self.configTab.rowconfigure(4, pad=10)
        self.configTab.columnconfigure(0, weight=1)

        #Filter List
        self.topConfigFrame     = ttk.Frame(self.configTab)
        self.topConfigFrame.grid(       column=0, row=0, sticky=tk.W+tk.E)
        self.topConfigFrame.columnconfigure( 0, weight=1)
        self.filterListScrollbar= ttk.Scrollbar(self.topConfigFrame, orient=tk.VERTICAL)
        self.filterListScrollbar.grid(  column=1, row=0, sticky=tk.N+tk.S, pady=2)
        self.filterListbox      = tk.Listbox(self.topConfigFrame, activestyle='underline', selectbackground=self.master.master.GlitchStyle.thirdColor, font=self.master.master.GlitchStyle.defaultFont, listvariable=self.master.master.filterListVar, height=4, yscrollcommand=self.filterListScrollbar)
        self.filterListbox.grid(        column=0, row=0, sticky=tk.W+tk.E, padx=3, pady=2)
        self.filterListScrollbar['command'] = self.filterListbox.yview

        self.firstSeperator     = ttk.Separator(self.configTab)
        self.firstSeperator.grid(       column=0, row=1, sticky=tk.W+tk.E)

        #Filter Config
        self.filterConfigFrame  = ttk.Frame(self.configTab)
        self.filterConfigFrame.grid(    column=0, row=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=5)
        self.filterConfigFrame.columnconfigure( 0, weight=1)
        self.filterConfigFrame.rowconfigure(    0, weight=1)

        self.secondSeperator    = ttk.Separator(self.configTab)
        self.secondSeperator.grid(      column=0, row=3, sticky=tk.W+tk.E)

        self.rgboffsetFilter = rgboffset.RGBoffsetFilter(self.filterConfigFrame, self)
        self.filterListObj.append(self.rgboffsetFilter)
        self.rgboffsetFilter.display_widgets()

        #Active Tab ****************************************************************************
        self.activeTab          = ttk.Frame(self.configbarNotebook)

        self.rgboffsetCheckbutton = ttk.Checkbutton(self.activeTab, text='RGB Offset', variable=self.rgboffsetFilter.activeState).grid(column=0, row=0)

        #Add childs to Notebook***************
        self.configbarNotebook.add(self.configTab, text='Config')
        self.configbarNotebook.add(self.activeTab, text='Active Filters')

        #All time showing Buttons****************************************
        self.bottomConfigFrame  = ttk.Frame(self)
        self.bottomConfigFrame.grid(    column=0, row=1, sticky=tk.W+tk.E, pady=10)
        self.bottomConfigFrame.columnconfigure( 0, weight=1)
        self.bottomConfigFrame.columnconfigure( 1, weight=1)
        self.bottomConfigFrame.rowconfigure(    0, weight=1, pad=5)
        self.bottomConfigFrame.rowconfigure(    1, weight=1, pad=5)

        self.applyButton        = ttk.Button(self.bottomConfigFrame, text='Apply Changes',              underline=0, command=self.apply_filter).grid(       column=0, row=0, sticky=tk.W+tk.E, padx=5)
        self.randomButton       = ttk.Button(self.bottomConfigFrame, text='Random Render',              underline=0, command=self.apply_filter_random).grid(column=1, row=0, sticky=tk.W+tk.E, padx=5)
        self.showRenderButton   = ttk.Button(self.bottomConfigFrame, text='Preview full sized Image',   underline=8, command=self.preview_image).grid(      column=0, row=1, sticky=tk.W+tk.E, padx=5, columnspan=2)

    def apply_filter_random(self, event=None):
        self.disable_configbar()
        image = copy(self.master.master.sourceImage)
        for filter in self.filterListObj:
            filter.random_values()
            image = filter.applyFilter(image)
        if image != None:
            self.master.master.tempImage = copy(image)
            del image
            self.master.master.tempImageThumbnail = self.master.master.menubar.create_thumbnail(self.master.master.tempImage)
            self.master.master.imagepreviewWidget.display_image(self.master.master.tempImageThumbnail)
        self.enable_configbar()

    def apply_filter(self, event=None):
        self.disable_configbar()
        image = copy(self.master.master.sourceImage)
        for filter in self.filterListObj:
            image = filter.applyFilter(image)
        self.master.master.tempImage = copy(image)
        del image
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
        changeState(self)
        self.master.master.master.update_idletasks()

    def enable_configbar(self):
        self.disable_configbar('!disabled')

