import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

class Imagepreview(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.grid(column=0, row=0, sticky='news')
        tk.Grid.columnconfigure(self, 0, weight=1)
        tk.Grid.rowconfigure(self, 0, weight=1)
        self.bind('<Configure>', func=self.resize_previewCanvas)

        self.init_widgets()

    def init_widgets(self):
        self.previewCanvas = tk.Canvas(self)
        self.previewCanvas.grid(    column=0, row=0, sticky='news')
        self.master.update_idletasks
        
    def resize_previewCanvas(self, event):
        self.previewCanvas.config(width=self.winfo_width(), height=self.winfo_height())
        self.display_image(self.master.tempImage)

    def display_image(self, image):
        if self.master.firstImageLoaded:
            scaleX = self.previewCanvas.winfo_width()  / image.width
            scaleY = self.previewCanvas.winfo_height() / image.height

            if(image.width >= image.height):
                if int(image.width * scaleY) < self.previewCanvas.winfo_width():
                    self.previewImage = ImageTk.PhotoImage(image.resize((int(image.width * scaleY), self.previewCanvas.winfo_height()), resample=Image.LANCZOS))
                else:
                    self.previewImage = ImageTk.PhotoImage(image.resize((self.previewCanvas.winfo_width(), int(image.height*scaleX)), resample=Image.LANCZOS))
            else:
                if int(image.width * scaleY) < self.previewCanvas.winfo_width():
                    self.previewImage = ImageTk.PhotoImage(image.resize((int(image.width * scaleY), self.previewCanvas.winfo_height()), resample=Image.LANCZOS))
                else:
                    self.previewImage = ImageTk.PhotoImage(image.resize((self.previewCanvas.winfo_width(), int(image.height*scaleX)), resample=Image.LANCZOS))

            self.previewCanvas.create_image(int((self.previewCanvas.winfo_width()-self.previewImage.width())/2), int((self.previewCanvas.winfo_height()-self.previewImage.height())/2), anchor=tk.NW, image=self.previewImage)