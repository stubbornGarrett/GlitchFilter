from PIL import Image, ImageTk
from copy import copy

sourceImage            = Image.new('RGB', (1,1), 'pink')
sourceImagePath        = ''
sourceImageExtension   = '.png'
sourceImageThumbnail   = copy(sourceImage)
tempImageThumbnail     = copy(sourceImage)
tempImage              = copy(sourceImage)

firstImageLoaded = False

FILEOPTIONS =  dict(   filetypes=[\
                        ('JPEG','*.jpg *.jpeg'),
                        ('PNG','*.png'),
                        ("all files","*.*")])

sizeMultiplicator = 1.0