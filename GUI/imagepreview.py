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

        self.init_widgets()

    def init_widgets(self):
        self.mainWindow.master.update_idletasks()
        self.previewCanvas = tk.Canvas(self,  highlightthickness=0)
        try:
            self.previewCanvas.config(background=self.mainWindow.backgroundColor)
        except:
            pass
        self.previewCanvas.grid(column=0, row=0)#, sticky='news')
        self.previewCanvas.bind('<MouseWheel>', func=self.update_size_multiplicator)
        
    def adjust_canvas_size(self, event=None):
        if self.mainWindow.firstImageLoaded:
            self.previewCanvas.config(width=self.winfo_width(), height=self.winfo_height())
            self.display_image()

    def update_size_multiplicator(self, event):
        if self.mainWindow.sizeMultiplicator >= 0.05 and event.delta < 0:
            if self.mainWindow.sizeMultiplicator >= 1:
                self.mainWindow.sizeMultiplicator -= 0.1
            else:
                self.mainWindow.sizeMultiplicator -= 0.05
        elif self.mainWindow.sizeMultiplicator <= 3 and event.delta > 0:
            if self.mainWindow.sizeMultiplicator >= 1:
                self.mainWindow.sizeMultiplicator += 0.2
            else:
                self.mainWindow.sizeMultiplicator += 0.05

        self.display_image()

    def update_preview_offset(self, event):
        stepsize = int(self.mainWindow.sourceImage.height/100*5)
        if event.keysym == 'Up'     and self.mainWindow.previewYoffset-stepsize > -self.mainWindow.sourceImageThumbnail.height/2:
            self.mainWindow.previewYoffset -= stepsize
        if event.keysym == 'Down'   and self.mainWindow.previewYoffset+stepsize < self.mainWindow.sourceImageThumbnail.height/2:
            self.mainWindow.previewYoffset += stepsize

        if event.keysym == 'Left'   and self.mainWindow.previewXoffset-stepsize > -self.mainWindow.sourceImageThumbnail.width/2:
            self.mainWindow.previewXoffset -= stepsize
        if event.keysym == 'Right'  and self.mainWindow.previewXoffset+stepsize < self.mainWindow.sourceImageThumbnail.width/2:
            self.mainWindow.previewXoffset += stepsize

        self.display_image()

    def display_image(self):
        if self.mainWindow.firstImageLoaded:
            if self.mainWindow.previewActiveVar.get():
                image = self.mainWindow.tempImageThumbnail
            else:
                image = self.mainWindow.sourceImageThumbnail

            scaleX = self.previewCanvas.winfo_width()  / image.width
            scaleY = self.previewCanvas.winfo_height() / image.height

            if int(image.width * scaleY) < self.previewCanvas.winfo_width():
                image = image.resize((int(image.width * scaleY * self.mainWindow.sizeMultiplicator), int(self.mainWindow.sizeMultiplicator * self.previewCanvas.winfo_height())), resample=Image.LANCZOS)
            else:
                image = image.resize((int(self.mainWindow.sizeMultiplicator * self.previewCanvas.winfo_width()), int(self.mainWindow.sizeMultiplicator * image.height*scaleX)), resample=Image.LANCZOS)

            self.previewImage = ImageTk.PhotoImage(image)

            if  self.mainWindow.previewYoffset >  self.previewImage.height()/2:
                self.mainWindow.previewYoffset =  self.previewImage.height()/2
            if  self.mainWindow.previewYoffset < -self.previewImage.height()/2:
                self.mainWindow.previewYoffset = -self.previewImage.height()/2
                
            if  self.mainWindow.previewXoffset >  self.previewImage.width()/2:
                self.mainWindow.previewXoffset =  self.previewImage.width()/2
            if  self.mainWindow.previewXoffset < -self.previewImage.width()/2:
                self.mainWindow.previewXoffset = -self.previewImage.width()/2

            self.previewCanvas.create_image(int((self.previewCanvas.winfo_width()-self.previewImage.width())/2)+self.mainWindow.previewXoffset, int((self.previewCanvas.winfo_height()-self.previewImage.height())/2)+self.mainWindow.previewYoffset, anchor=tk.NW, image=self.previewImage)
            #self.previewCanvas.create_image(int((self.previewCanvas.winfo_width()-self.previewImage.width())/2)-self.mainWindow.previewXoffset, int((self.previewCanvas.winfo_height()-self.previewImage.height())/2)-self.mainWindow.previewYoffset, anchor=tk.NW, image=self.previewImage)

    def crop_image(self, canvas, image):
        iHeight = image.height
        iWidth  = image.width
        cHeight = self.previewCanvas.winfo_height()
        cWidth  = self.previewCanvas.winfo_width()
        yOffset = self.mainWindow.previewYoffset
        xOffset = self.mainWindow.previewXoffset
        multi   = self.mainWindow.sizeMultiplicator

        leftEdge    = int((cWidth  - iWidth)  / 2)
        topEdge     = int((cHeight - iHeight) / 2)

        leftEdge    = 0         if leftEdge >= 0+xOffset*multi    else -leftEdge+xOffset
        topEdge     = 0         if topEdge  >= 0+yOffset*multi    else -topEdge +yOffset

        rightEdge   = iWidth    if leftEdge == 0    else iWidth -leftEdge
        bottomEdge  = iHeight   if topEdge  == 0    else iHeight-topEdge

        if xOffset > 0 and rightEdge+xOffset*multi > cWidth:
            rightEdge -= rightEdge+xOffset*multi-cWidth
#        elif xOffset < 0 and leftEdge + xOffset > cWidth:
#            leftEdge -= xOffset

        timage = image.crop((leftEdge, topEdge, rightEdge, bottomEdge))

        timage.save('./pic/pic1.jpg')

        image = ImageTk.PhotoImage(image.crop((leftEdge, topEdge, rightEdge, bottomEdge)))
        

        return image