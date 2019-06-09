from tkinter.ttk import Frame, Label
import tkinter as tk

class Infobar(Frame):
    def __init__(self, parentWidget=None, backgroundcolor='#cccccc', foregroundcolor='#111111', font=('Arial', '8'), text=' -'):
        '''
        ...
        '''
        Frame.__init__(self, parentWidget, relief='ridge', borderwidth=1)
        self.columnconfigure(   0, weight=1)
        self.rowconfigure(      0, weight=1)

        self.imageInfoVar       = tk.StringVar()
        self.imageInfoVar.set(text)
        self.imageInfoLabel     = Label(self, anchor=tk.W, background=backgroundcolor, foreground=foregroundcolor, font=font, textvariable=self.imageInfoVar, padding=0)
        self.imageInfoLabel.grid(   column=0, row=0, sticky='we')#, padx=2, pady=2)

        self.previewInfoVar    = tk.StringVar()
        self.previewInfoVar.set('')
        self.previewInfoLabel   = Label(self, anchor=tk.W, background=backgroundcolor, foreground=foregroundcolor, font=font, textvariable=self.previewInfoVar, padding=0)
        self.previewInfoLabel.grid( column=1, row=0, sticky='e')#, padx=2, pady=2)

    def update_imageInfo(self, text=' '):
        self.imageInfoVar.set(text)

    def update_previewInfo(self, text='x1.0'):
        self.previewInfoVar.set(text)