import tkinter as tk
import tkinter.ttk as ttk

class Configbar(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master, width=400)
        self.grid(column=1, row=0, sticky='ns')
        tk.Grid.rowconfigure(self, 0, weight=1)

        self.init_widgets()

    def init_widgets(self):
        self.imageCanvas = tk.Canvas(self, bg='blue')
        self.imageCanvas.grid(column=0, row=0, sticky=tk.N+tk.E+tk.S+tk.W)