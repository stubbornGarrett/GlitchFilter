from tools import logger
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from copy import copy

class Imagepreview(ttk.Frame):
    def __init__(self, master=None, mainWindow=None):
        ttk.Frame.__init__(self, master)
        self.mainWindow = mainWindow
        self.bind('<Configure>', self.adjust_canvas_size)
        self.previewImage = copy(self.mainWindow.sourceImage)
        self.canvasScale        = 1.0
        self.previewImage_ID    = None

        self.init_widgets()
        #self.previewCanvas.config(scrollregion=self.previewCanvas.bbox(tk.ALL))

        self.canvasZeroX = self.previewCanvas.xview()[0]
        self.canvasZeroY = self.previewCanvas.yview()[0]
        self.previewCanvas.bind("<ButtonPress-1>", self.scroll_start)
        self.previewCanvas.bind("<B1-Motion>", self.scroll_move)
        self.previewCanvas.bind('<MouseWheel>', func=self.zoom)

    def init_widgets(self):
        self.mainWindow.master.update_idletasks()
        self.previewCanvas = tk.Canvas(self, highlightthickness=0)
        try:
            self.previewCanvas.config(background=self.mainWindow.backgroundColor)
        except:
            pass
        self.previewCanvas.grid(column=0, row=0)#, sticky='news')

    def adjust_canvas_size(self, event=None):
        self.previewCanvas.config(width=self.winfo_width(), height=self.winfo_height())
        if self.mainWindow.firstImageLoaded:
            if self.mainWindow.sourceImage.height/self.previewCanvas.winfo_height() > self.mainWindow.sourceImage.width/self.previewCanvas.winfo_width():
                self.canvasScale = self.previewCanvas.winfo_height() / self.previewImage.height
            else:
                self.canvasScale = self.previewCanvas.winfo_width() / self.previewImage.width
            self.display_image(self.select_active_image())

    def scroll_start(self, event):
        self.previewCanvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.previewCanvas.scan_dragto(event.x, event.y, gain=1)
        self.display_image(self.select_active_image())

    def zoom(self, event):
        if event.delta >= 0 and self.canvasScale < 20:
            self.canvasScale *= 1.2
        if event.delta <  0 and self.canvasScale > 0.1:
            self.canvasScale *= 1/1.2
        self.display_image(self.select_active_image(), event.x, event.y)

    def display_image(self, image, x=0, y=0):
        if self.previewImage_ID:
            self.previewCanvas.delete(self.previewImage_ID)

        scaleWidth, scaleHeight = int(image.width*(self.canvasScale)), int(image.height*(self.canvasScale))
        size    = scaleWidth, scaleHeight
        image   = image.resize(size, resample=Image.LANCZOS)

        z = int((self.previewCanvas.winfo_width()-scaleWidth)/2)+1
        y = int((self.previewCanvas.winfo_height()-scaleHeight)/2)+1

        if self.previewCanvas.canvasx(0) > z:
            leftEdge = self.previewCanvas.canvasx(0) - z
        else:
            leftEdge = 0

        if scaleWidth+z-(self.previewCanvas.canvasx(0)) > self.previewCanvas.winfo_width():
            rightEdge = scaleWidth+(z+self.previewCanvas.canvasx(0))
        else:
            rightEdge = image.width

        if self.previewCanvas.canvasy(0) > y:
            topEdge = self.previewCanvas.canvasy(0) - y
        else:
            topEdge = 0
        
        if scaleHeight+y-(self.previewCanvas.canvasy(0)) > self.previewCanvas.winfo_height():
            bottomEdge = scaleHeight+(y+self.previewCanvas.canvasy(0))
        else:
            bottomEdge = image.height

        image = image.crop((leftEdge, topEdge, rightEdge, bottomEdge))

        # draw
        x = self.previewCanvas.winfo_width() / 2 + (leftEdge + rightEdge  - scaleWidth)  /2
        y = self.previewCanvas.winfo_height()/ 2 + (topEdge  + bottomEdge - scaleHeight) /2
        self.mainWindow.previewImage = ImageTk.PhotoImage(image)
        self.previewImage_ID            = self.previewCanvas.create_image(x, y, image=self.mainWindow.previewImage)
        self.previewCanvas.scale(tk.ALL, x, y,self.canvasScale, self.canvasScale)


    def reset_preview_values(self, event=None):
        self.canvasScale = 1.0
        self.previewCanvas.xview_moveto(self.canvasZeroX)
        self.previewCanvas.yview_moveto(self.canvasZeroY)
        self.adjust_canvas_size()

    def select_active_image(self):
        if self.mainWindow.previewActiveVar.get():
            return self.mainWindow.tempImage
        else:
            return self.mainWindow.sourceImage
