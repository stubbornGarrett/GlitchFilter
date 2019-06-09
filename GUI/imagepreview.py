from tools import logger
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from copy import copy
import time

class Imagepreview(ttk.Frame):
    def __init__(self, parentWidget=None, image=None, backgroundcolor='#999999', zoomscale=1.2, minzoomlevel=0.1, maxzoomlevel=3, quality=0):
        '''
        A tkinter Frame, which contains a canvas. The canvas adapts to the size of the frame.\n
        parentWidget: Widget wich will contain this class (e.g. Tk root window).\n
        image: The image, which will be displayed on the canvas (can be changed with '.update_image(*PIL.Image*)').\n
        backgroundcolor: Color of whitespace on canvas.\n
        zoomscale: If the mouse is inside the canvas and the mousewheel gets triggered (Up/Down), the image is scaled by this factor.\n
        minzoom/maxzoom: Minimum and maximum value, for scaling the image.\n
        quality: 0-4 Different operations to resize image [NEAREST, BILINEAR, HAMMING, BICUBIC, LANCZOS]
        '''
        ttk.Frame.__init__(self, parentWidget)
        self.previewImage    = image
        self.resizedImage    = None
        self.canvasImage     = None

        if self.previewImage != None:
            self.imageLoaded = True
        else:
            self.imageLoaded = False

        self.previewImage_ID = None
        self.canvasScale     = 1.0
        self.scaleChanged    = False
        self.update_zoom_settings(zoomscale, minzoomlevel, maxzoomlevel)

        self.resizeFilter    = [Image.NEAREST, Image.BILINEAR, Image.HAMMING, Image.BICUBIC, Image.LANCZOS]
        self.resizeQuality   = quality

        if self.imageLoaded:
            self.resizeWidth, self.resizeHeight = int(self.previewImage.width*(self.canvasScale)), int(self.previewImage.height*(self.canvasScale))
            self.resizeSize = self.resizeWidth, self.resizeHeight
            self.whiteSpaceX = int((self.previewCanvas.winfo_width() -self.resizeWidth) /2)+1
            self.whiteSpaceY = int((self.previewCanvas.winfo_height()-self.resizeHeight)/2)+1

        self.init_canvas(backgroundcolor)
        self.create_binds()#)

        self.canvasZeroX = self.previewCanvas.xview()[0]
        self.canvasZeroY = self.previewCanvas.yview()[0]

    def init_canvas(self, color):
        self.previewCanvas = tk.Canvas(self, highlightthickness=0, bg=color)
        self.previewCanvas.grid(column=0, row=0)

    def create_binds(self):#, zoomscale, minzoomlevel, maxzoomlevel):
        self.bind('<Configure>', self.adjust_canvas_size)
        self.previewCanvas.bind('<ButtonPress-1>',  self.scroll_start)
        self.previewCanvas.bind('<B1-Motion>',      self.scroll_move)
        # self.previewCanvas.bind('<MouseWheel>',     lambda e: self.zoom(e, zoomscale, minzoomlevel, maxzoomlevel))

    def adjust_canvas_size(self, event=None):
        self.previewCanvas.config(width=self.winfo_width(), height=self.winfo_height())
        if self.imageLoaded:
            self.display_image(image=self.previewImage, quality=self.resizeQuality)

    def scroll_start(self, event):
        self.previewCanvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.previewCanvas.scan_dragto(event.x, event.y, gain=1)

        if self.previewCanvas.canvasx(0) > self.whiteSpaceX \
        or self.resizeWidth +self.whiteSpaceX-(self.previewCanvas.canvasx(0)) > self.previewCanvas.winfo_width() \
        or self.previewCanvas.canvasy(0) > self.whiteSpaceY \
        or self.resizeHeight+self.whiteSpaceY-(self.previewCanvas.canvasy(0)) > self.previewCanvas.winfo_height():
            self.display_image(image=self.previewImage, quality=self.resizeQuality)

    def update_zoom_settings(self, scale, minlevel, maxlevel):
        self.zoomscale = scale
        self.minlevel  = minlevel
        self.maxlevel  = maxlevel

    def zoom(self, event):
        if event.delta >= 0 and self.canvasScale < self.maxlevel:
            self.canvasScale *= self.zoomscale
        if event.delta <  0 and self.canvasScale > self.minlevel:
            self.canvasScale *= 1/self.zoomscale
        self.scaleChanged = True
        self.display_image(event.x, event.y, self.previewImage, self.resizeQuality)

    def update_image(self, image=None):
        self.previewImage = image
        self.resizedImage = image
        self.imageLoaded = False if self.previewImage == None else True
        if self.imageLoaded:
            self.resizeWidth, self.resizeHeight = int(self.previewImage.width*(self.canvasScale)), int(self.previewImage.height*(self.canvasScale))
            self.resizeSize = self.resizeWidth, self.resizeHeight
            self.whiteSpaceX = int((self.previewCanvas.winfo_width() -self.resizeWidth) /2)+1
            self.whiteSpaceY = int((self.previewCanvas.winfo_height()-self.resizeHeight)/2)+1

            self.display_image(image=self.previewImage, quality=self.resizeQuality)
        else:
            self.previewCanvas.delete(self.previewImage_ID)

    def display_image(self, x=0, y=0, image=None, quality=0):
        if self.imageLoaded:
            if self.previewImage_ID:
                self.previewCanvas.delete(self.previewImage_ID)

            self.resizeWidth, self.resizeHeight = int(self.previewImage.width*self.canvasScale), int(self.previewImage.height*self.canvasScale)
            self.resizeSize  = self.resizeWidth, self.resizeHeight
            self.whiteSpaceX = int((self.previewCanvas.winfo_width() -self.resizeWidth) /2)+1
            self.whiteSpaceY = int((self.previewCanvas.winfo_height()-self.resizeHeight)/2)+1
            if self.scaleChanged:
                self.resizedImage = image.resize(self.resizeSize, resample=self.resizeFilter[quality])
                self.scaleChanged = False

            leftEdge    = self.previewCanvas.canvasx(0)-self.whiteSpaceX  if self.previewCanvas.canvasx(0) > self.whiteSpaceX  else 0
            rightEdge   = self.resizeWidth +(self.whiteSpaceX+self.previewCanvas.canvasx(0)) if self.resizeWidth +self.whiteSpaceX-(self.previewCanvas.canvasx(0)) > self.previewCanvas.winfo_width()  else self.resizedImage.width
            topEdge     = self.previewCanvas.canvasy(0)-self.whiteSpaceY  if self.previewCanvas.canvasy(0) > self.whiteSpaceY  else 0
            bottomEdge  = self.resizeHeight+(self.whiteSpaceY+self.previewCanvas.canvasy(0)) if self.resizeHeight+self.whiteSpaceY-(self.previewCanvas.canvasy(0)) > self.previewCanvas.winfo_height() else self.resizedImage.height

            x = self.previewCanvas.winfo_width() / 2 + (leftEdge + rightEdge  - self.resizeWidth)  /2
            y = self.previewCanvas.winfo_height()/ 2 + (topEdge  + bottomEdge - self.resizeHeight) /2
            if rightEdge - leftEdge > 0 and bottomEdge - topEdge > 0:
                cropedImage = self.resizedImage.crop((leftEdge, topEdge, rightEdge, bottomEdge))
                self.canvasImage = ImageTk.PhotoImage(cropedImage)
                self.previewImage_ID = self.previewCanvas.create_image(x, y, image=self.canvasImage)

            self.previewCanvas.scale(tk.ALL, x, y, self.canvasScale, self.canvasScale)

    def original_zoom(self, event=None):
        self.canvasScale  = 1.0
        self.scaleChanged = True
        self.display_image(image=self.previewImage, quality=self.resizeQuality)

    def reset_preview(self, event=None):
        if self.previewImage.height/self.previewCanvas.winfo_height() > self.previewImage.width/self.previewCanvas.winfo_width():
            self.canvasScale  = self.previewCanvas.winfo_height() / self.previewImage.height
            self.scaleChanged = True
        else:
            self.canvasScale  = self.previewCanvas.winfo_width()  / self.previewImage.width
            self.scaleChanged = True
        self.previewCanvas.xview_moveto(self.canvasZeroX)
        self.previewCanvas.yview_moveto(self.canvasZeroY)
        self.adjust_canvas_size()
