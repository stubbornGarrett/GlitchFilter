from tools import logger
import tkinter as tk
import tkinter.ttk as ttk
from Filters import rgboffset, bigblocks, screenlines, burningnoise
from copy import copy

class Configbar(ttk.Frame):
    def __init__(self, master=None, mainWindow=None):
        ttk.Frame.__init__(self, master)#, width=400)
        self.mainWindow = mainWindow

        #self.rowconfigure(1, pad=10)
        #self.rowconfigure(2, weight=1)
        #self.rowconfigure(3, pad=10)
        #self.rowconfigure(4, pad=10)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.inProgress = False

        self.filterListObj = []
        self.init_widgets()

        self.filterListbox.bind('<<ListboxSelect>>',           self.update_filter_selection)
        self.configTab.bind(    '<Configure>',       lambda e: self.filterConfigCanvas.itemconfig(self.filterConfigCanvasWindow, width=self.configTab.winfo_width()))

    def init_widgets(self):
        self.configbarNotebook  = ttk.Notebook(self)
        self.configbarNotebook.grid(column=0, row=0, sticky='news')

        #Confgig Tab ****************************************************************************
        self.configTab          = ttk.Frame(self.configbarNotebook)

        self.configTab.rowconfigure(0, pad=10)
        #self.configTab.rowconfigure(1)
        self.configTab.rowconfigure(2, weight=1)
        self.configTab.rowconfigure(3)#, pad=10)
        self.configTab.columnconfigure(0, weight=1)

        #Filter Listbox
        self.topConfigFrame     = ttk.Frame(self.configTab)
        self.topConfigFrame.grid(       column=0, row=0, sticky=tk.W+tk.E)
        self.topConfigFrame.columnconfigure( 0, weight=1)
        self.filterListScrollbar= ttk.Scrollbar(self.topConfigFrame, orient=tk.VERTICAL)
        self.filterListScrollbar.grid(  column=1, row=0, sticky=tk.N+tk.S, pady=2)
        self.filterListbox      = tk.Listbox(self.topConfigFrame, listvariable=self.mainWindow.filterListVar, activestyle='none', height=4, yscrollcommand=self.filterListScrollbar)
        try:
            self.filterListbox.config(selectbackground=self.mainWindow.highlightsColor, font='({},{})'.format(self.mainWindow.defaultFont, self.mainWindow.defaultFontSize))
        except:
            pass

        self.filterListbox.grid(        column=0, row=0, sticky=tk.W+tk.E, padx=3, pady=2)
        self.filterListScrollbar['command'] = self.filterListbox.yview

        self.firstSeperator     = ttk.Separator(self.configTab)
        self.firstSeperator.grid(       column=0, row=1, sticky=tk.W+tk.E)#, pady=5)

        #Filter Config
        self.filterConfigCanvas     = tk.Canvas(self.configTab, bd=0, highlightthickness=0)
        self.filterConfigScrollbar  = ttk.Scrollbar(self.configTab, orient=tk.VERTICAL, command=self.filterConfigCanvas.yview)
        self.filterConfigCanvas.configure(yscrollcommand=self.filterConfigScrollbar.set)
        self.filterConfigCanvas.grid(column=0, row=2, sticky=tk.W+tk.E+tk.N)#+tk.S)
        self.filterConfigCanvas.columnconfigure(0, weight=1)
        self.filterConfigCanvas.rowconfigure(0, weight=1)
        try:
            self.filterConfigCanvas.config(background=self.mainWindow.backgroundColor)
        except:
            pass
        self.filterConfigFrame      = ttk.Frame(self.filterConfigCanvas, relief='sunken', borderwidth=5, pad=3)
        self.filterConfigCanvasWindow = self.filterConfigCanvas.create_window(0,0, anchor='nw', window=self.filterConfigFrame)

        #Prepare Filters*****************************************************************
        # RGB Offset 
        self.rgboffsetFilter    = rgboffset.RGBoffsetFilter(self.filterConfigFrame, self)
        self.filterListObj.append(self.rgboffsetFilter)
        self.mainWindow.filterListStr.append(self.rgboffsetFilter.name)
        self.rgboffsetFilter.display_widgets()

        # Big Blocks Offset
        self.bigblocksFilter    = bigblocks.BigBlocksFilter(self.filterConfigFrame, self)
        self.filterListObj.append(self.bigblocksFilter)
        self.mainWindow.filterListStr.append(self.bigblocksFilter.name)

        # Screen Lines
        self.screenlinesFilter  = screenlines.ScreenLinesFilter(self.filterConfigFrame, self)
        self.filterListObj.append(self.screenlinesFilter)
        self.mainWindow.filterListStr.append(self.screenlinesFilter.name)

        # Burning Noise
        self.burningnoiseFilter = burningnoise.BurningNoiseFilter(self.filterConfigFrame, self)
        self.filterListObj.append(self.burningnoiseFilter)
        self.mainWindow.filterListStr.append(self.burningnoiseFilter.name)


        self.mainWindow.filterListVar.set(self.mainWindow.filterListStr)

        self.filterConfigFrame.update_idletasks()
        self.filterConfigCanvas.configure(scrollregion=self.filterConfigCanvas.bbox('all'), height=self.filterConfigFrame.winfo_height())

        #Active Filter Tab ****************************************************************
        self.activeTab          = ttk.Frame(self.configbarNotebook)

        self.checkButtonFrame   = ttk.Frame(self.activeTab)
        self.checkButtonFrame.grid(column=0, row=0, padx=5, pady=2, sticky=tk.W+tk.N)

        self.rgboffsetCheckbutton    = ttk.Checkbutton(self.checkButtonFrame, text='RGB Offset',         variable=self.rgboffsetFilter.activeState).grid(    column=0, row=0, sticky=tk.W)
        self.bigblocksCheckbutton    = ttk.Checkbutton(self.checkButtonFrame, text='Big Blocks Offset',  variable=self.bigblocksFilter.activeState).grid(    column=0, row=1, sticky=tk.W)
        self.screenlinesCheckbutton  = ttk.Checkbutton(self.checkButtonFrame, text='Screen Lines',       variable=self.screenlinesFilter.activeState).grid(  column=0, row=2, sticky=tk.W)
        self.burningnoiseCheckbutton = ttk.Checkbutton(self.checkButtonFrame, text='Burning Noise',      variable=self.burningnoiseFilter.activeState).grid( column=0, row=3, sticky=tk.W)
        
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

        self.applyButton        = ttk.Button(       self.bottomConfigFrame, text='Apply Changes',              underline=0, command=self.apply_filter)
        self.applyButton.grid(                                                column=0, row=0, sticky='news'   , padx=5, pady=2, rowspan=2)
        self.randomButton       = ttk.Button(       self.bottomConfigFrame, text='Random Render',              underline=0, command=self.apply_filter_random)
        self.randomButton.grid(                                         column=1, row=0, sticky=tk.W+tk.E, padx=5)
        self.showRenderButton   = ttk.Button(       self.bottomConfigFrame, text='Preview full sized Image',   underline=8, command=self.preview_image)
        self.showRenderButton.grid(                                               column=1, row=1, sticky=tk.W+tk.E, padx=5)
        self.previewCheckbutton = ttk.Checkbutton(  self.bottomConfigFrame, text='Preview', variable=self.mainWindow.previewActiveVar, command=self.mainWindow.imagepreviewWidget.display_image)
        self.previewCheckbutton.grid( column=0, row=2, sticky=tk.W,      padx=3)
        self.resetPreviewButton = ttk.Button(       self.bottomConfigFrame, text='Reset Preview (Ctrl+X)',                  command=self.mainWindow.imagepreviewWidget.reset_preview_values)
        self.resetPreviewButton.grid(                                               column=1, row=2, sticky=tk.W+tk.E, padx=5)

    def apply_filter_random(self, event=None):
        if self.mainWindow.firstImageLoaded:
            self.disable_configbar()
            image = copy(self.mainWindow.sourceImage)
            for filter in self.filterListObj:
                filter.random_values()
                filter.update_widgets_config()
                image = filter.applyFilter(image)
            self.mainWindow.tempImage = copy(image)
            del image
            self.mainWindow.imagepreviewWidget.display_image(self.mainWindow.imagepreviewWidget.select_active_image())
            self.enable_configbar()

    def apply_filter(self, event=None):
        if self.mainWindow.firstImageLoaded:
            self.disable_configbar()
            image = copy(self.mainWindow.sourceImage)
            for filter in self.filterListObj:
                image = filter.applyFilter(image)
            self.mainWindow.tempImage = copy(image)
            del image
            self.mainWindow.imagepreviewWidget.display_image(self.mainWindow.imagepreviewWidget.select_active_image())
            self.enable_configbar()

    def update_filter_selection(self, event):
        #Get Name of the selected Filter as a String
        selection = self.mainWindow.filterListStr[int(' '.join(map(str, self.filterListbox.curselection())))] #self.filterListbox.selection_get()

        for child in self.filterConfigFrame.winfo_children():
            child.grid_forget()

        if selection == self.rgboffsetFilter.name:
            self.rgboffsetFilter.display_widgets()

        if selection == self.bigblocksFilter.name:
            self.bigblocksFilter.display_widgets()

        if selection == self.screenlinesFilter.name:
            self.screenlinesFilter.display_widgets()

        if selection == self.burningnoiseFilter.name:
            self.burningnoiseFilter.display_widgets()

        # Update canvas window size
        self.filterConfigFrame.update_idletasks()
        self.filterConfigCanvas.configure(scrollregion=self.filterConfigCanvas.bbox('all'), height=self.filterConfigFrame.winfo_height())

    def preview_image(self, event=None):
        if self.mainWindow.firstImageLoaded:
            try:
                self.mainWindow.tempImage.show()
            except:
                # ERROR
                pass

    # def disable_configbar(self, state='disabled'):
    #     self.inProgress = True
    #     self.filterListbox.config(state=state)
    #     #self.filterListScrollbar.config(state=state)
    #     self.applyButton.config(state=state)
    #     self.randomButton.config(state=state)
    #     self.showRenderButton.config(state=state)
    #     self.previewCheckbutton.config(state=state)
    #     self.resetPreviewButton.config(state=state)

    #     print(int(self.filterListbox.curselection()[1]))

    #     if state == 'normal' and self.filterListObj[int(self.filterListbox.curselection()[0])].activeState == 1:
    #         for child in self.filterListObj[self.filterListbox.curselection()].cageFrame.winfo_children():
    #             try:
    #                 child.configure(state='normal')
    #             except:
    #                 pass

    #     elif state == 'disable':
    #         for child in self.filterListObj[int(self.filterListbox.curselection()[0])].cageFrame.winfo_children():
    #             try:
    #                 child.configure(state='disable')
    #             except:
    #                 pass

    #     self.mainWindow.master.update_idletasks()

    def enable_configbar(self):
        self.disable_configbar('normal')
        self.inProgress = False


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
        self.mainWindow.master.update_idletasks()