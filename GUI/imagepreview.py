from tools import logger
import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
from copy import copy

class Imagepreview(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.bind('<Configure>',    self.adjust_canvas_size)
        self.previewImage = copy(self.master.master.sourceImage)

        self.init_widgets()

    def init_widgets(self):
        self.master.master.master.update_idletasks()
        self.previewCanvas = tk.Canvas(self,  highlightthickness=0, background=self.master.master.GlitchStyle.firstColor)
        self.previewCanvas.grid(column=0, row=0)#, sticky='news')
        self.previewCanvas.bind('<MouseWheel>', func=self.update_size_multiplicator)
        
    def adjust_canvas_size(self, event=None):
        if self.master.master.firstImageLoaded:
            self.previewCanvas.config(width=self.winfo_width(), height=self.winfo_height())
            self.display_image()

    def update_size_multiplicator(self, event):
        if self.master.master.sizeMultiplicator >= 0.05 and event.delta < 0:
            if self.master.master.sizeMultiplicator >= 1:
                self.master.master.sizeMultiplicator -= 0.1
            else:
                self.master.master.sizeMultiplicator -= 0.05
        elif self.master.master.sizeMultiplicator <= 3 and event.delta > 0:
            if self.master.master.sizeMultiplicator >= 1:
                self.master.master.sizeMultiplicator += 0.2
            else:
                self.master.master.sizeMultiplicator += 0.05

        self.display_image()

    def update_preview_offset(self, event):
        stepsize = int(self.master.master.sourceImage.height/100*5)
        if event.keysym == 'Up' and self.master.master.previewYoffset-stepsize > -self.master.master.sourceImageThumbnail.height/2:
            self.master.master.previewYoffset -= stepsize
        if event.keysym == 'Down' and self.master.master.previewYoffset+stepsize < self.master.master.sourceImageThumbnail.height/2:
            self.master.master.previewYoffset += stepsize

        if event.keysym == 'Left' and self.master.master.previewXoffset-stepsize > -self.master.master.sourceImageThumbnail.width/2:
            self.master.master.previewXoffset -= stepsize
        if event.keysym == 'Right' and self.master.master.previewXoffset+stepsize < self.master.master.sourceImageThumbnail.width/2:
            self.master.master.previewXoffset += stepsize

        self.display_image()

    def display_image(self):
        if self.master.master.firstImageLoaded:
            if self.master.master.previewActiveVar.get():
                image = self.master.master.tempImageThumbnail
            else:
                image = self.master.master.sourceImageThumbnail

            scaleX = self.previewCanvas.winfo_width()  / image.width
            scaleY = self.previewCanvas.winfo_height() / image.height

            if int(image.width * scaleY) < self.previewCanvas.winfo_width():
                image = image.resize((int(image.width * scaleY * self.master.master.sizeMultiplicator), int(self.master.master.sizeMultiplicator * self.previewCanvas.winfo_height())), resample=Image.LANCZOS)
            else:
                image = image.resize((int(self.master.master.sizeMultiplicator * self.previewCanvas.winfo_width()), int(self.master.master.sizeMultiplicator * image.height*scaleX)), resample=Image.LANCZOS)

            #self.previewImage = self.crop_image(self.previewCanvas, image)
            self.previewImage = ImageTk.PhotoImage(image)

            if  self.master.master.previewYoffset >  self.previewImage.height()/2:
                self.master.master.previewYoffset =  self.previewImage.height()/2
            if  self.master.master.previewYoffset < -self.previewImage.height()/2:
                self.master.master.previewYoffset = -self.previewImage.height()/2
                
            if  self.master.master.previewXoffset >  self.previewImage.width()/2:
                self.master.master.previewXoffset =  self.previewImage.width()/2
            if  self.master.master.previewXoffset < -self.previewImage.width()/2:
                self.master.master.previewXoffset = -self.previewImage.width()/2

            self.previewCanvas.create_image(int((self.previewCanvas.winfo_width()-self.previewImage.width())/2)+self.master.master.previewXoffset, int((self.previewCanvas.winfo_height()-self.previewImage.height())/2)+self.master.master.previewYoffset, anchor=tk.NW, image=self.previewImage)
            #self.previewCanvas.create_image(int((self.previewCanvas.winfo_width()-self.previewImage.width())/2)-self.master.master.previewXoffset, int((self.previewCanvas.winfo_height()-self.previewImage.height())/2)-self.master.master.previewYoffset, anchor=tk.NW, image=self.previewImage)

    def crop_image(self, canvas, image):
        iHeight = image.height
        iWidth  = image.width
        cHeight = self.previewCanvas.winfo_height()
        cWidth  = self.previewCanvas.winfo_width()
        yOffset = self.master.master.previewYoffset
        xOffset = self.master.master.previewXoffset
        multi   = self.master.master.sizeMultiplicator

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