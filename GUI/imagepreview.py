import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk

class Imagepreview(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.sizeMultiplicator = 1.0
        self.bind('<Configure>', func=self.adjust_canvas_size)

        self.init_widgets()

    def init_widgets(self):
        self.previewCanvas = tk.Canvas(self)
        self.previewCanvas.grid(column=0, row=0)#, sticky='news')
        self.previewCanvas.bind('<MouseWheel>', func=self.update_size_multiplicator)
        
    def adjust_canvas_size(self, event):
        self.previewCanvas.config(width=self.winfo_width(), height=self.winfo_height())
        self.display_image(self.master.tempImage)

    def update_size_multiplicator(self, event):
        if self.sizeMultiplicator >= 0.05 and event.delta < 0:
            if self.sizeMultiplicator >= 1:
                self.sizeMultiplicator -= 0.1
            else:
                self.sizeMultiplicator -= 0.05
        elif self.sizeMultiplicator <= 3 and event.delta > 0:
            if self.sizeMultiplicator >= 1:
                self.sizeMultiplicator += 0.1
            else:
                self.sizeMultiplicator += 0.05
        print(self.sizeMultiplicator)
        self.adjust_canvas_size(event=None)

    def display_image(self, image):
        if self.master.firstImageLoaded:
            scaleX = self.previewCanvas.winfo_width()  / image.width
            scaleY = self.previewCanvas.winfo_height() / image.height

            if int(image.width * scaleY) < self.previewCanvas.winfo_width():
                tempImage = image.resize((int(image.width * scaleY * self.sizeMultiplicator), int(self.sizeMultiplicator * self.previewCanvas.winfo_height())), resample=Image.LANCZOS)
            else:
                tempImage = image.resize((int(self.sizeMultiplicator * self.previewCanvas.winfo_width()), int(self.sizeMultiplicator * image.height*scaleX)), resample=Image.LANCZOS)

            if tempImage.height > self.previewCanvas.winfo_height() and tempImage.width < self.previewCanvas.winfo_width():
                self.previewImage = ImageTk.PhotoImage(tempImage.crop((0, int((tempImage.height-self.previewCanvas.winfo_height())/2), tempImage.width, self.previewCanvas.winfo_height()-int((self.previewCanvas.winfo_height()-tempImage.height)/2))))
            elif tempImage.height < self.previewCanvas.winfo_height() and tempImage.width > self.previewCanvas.winfo_width():
                self.previewImage = ImageTk.PhotoImage(tempImage.crop((int((tempImage.width-self.previewCanvas.winfo_width())/2), 0, self.previewCanvas.winfo_width()-int((self.previewCanvas.winfo_width()-tempImage.width)/2), tempImage.height)))
            elif tempImage.height > self.previewCanvas.winfo_height() and tempImage.width > self.previewCanvas.winfo_width():
                self.previewImage = ImageTk.PhotoImage(tempImage.crop((int((tempImage.width-self.previewCanvas.winfo_width())/2), int((tempImage.height-self.previewCanvas.winfo_height())/2), self.previewCanvas.winfo_width()-int((self.previewCanvas.winfo_width()-tempImage.width)/2), self.previewCanvas.winfo_height()-int((self.previewCanvas.winfo_height()-tempImage.height)/2))))
            else:
                self.previewImage = ImageTk.PhotoImage(tempImage)

            self.previewCanvas.create_image(int((self.previewCanvas.winfo_width()-self.previewImage.width())/2), int((self.previewCanvas.winfo_height()-self.previewImage.height())/2), anchor=tk.NW, image=self.previewImage)

            #self.previewImage = ImageTk.PhotoImage(tempImage.crop((int((tempImage.width-self.previewCanvas.winfo_width())/2), int((tempImage.height-self.previewCanvas.winfo_height())/2), self.previewCanvas.winfo_width()-int((self.previewCanvas.winfo_width()-tempImage.width)/2), self.previewCanvas.winfo_height()-int((self.previewCanvas.winfo_height()-tempImage.height)/2))))