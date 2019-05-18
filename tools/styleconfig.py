import tkinter as tk
import tkinter.ttk as ttk

class GlitchStyle(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        
        self.firstColor         = '#333333' #Background
        self.secondColor        = '#eeeeee' #Font
        self.thirdColor         = '#00aaaa' #Highlights (e.g. hovering a button)
        self.disableColor       = '#555555'
        self.disableFont        = '#999999'
        self.theme_create('GlitchTheme', settings={
            '.':                {'configure': { 'background'    : self.firstColor,
                                                'foreground'    : self.secondColor,
                                                'highlightcolor': self.thirdColor,
                                                'font'          : ("Calibri", 12),
                                                'relief'        : 'flat'}},

            'TLabel':           {'configure': { 'font'          : ("Calibri", 12),
                                                'padding'       : 3,
                                                'borderwidth'   : 1,
                                                'relief'        : 'groove'},
                                'map'       : { 'background'    : [('disabled', self.disableColor)],
                                                'foreground'    : [('disabled', self.disableFont)]}},

            'TCheckbutton':     {'configure': { 'background'    : self.firstColor,
                                                'foreground'    : self.secondColor}},

            'TButton':          {'configure': { 'font'          : ("Calibri", 12),
                                                'padding'       : 2,
                                                'borderwidth'   : 3,
                                                'justify'       : tk.CENTER,
                                                'relief'        : tk.RAISED},
                                'map'       : { 'background'    : [('active', self.thirdColor)],
                                                'relief'        : [('pressed', tk.SUNKEN)],
                                                'background'    : [('disabled', self.disableColor)],
                                                'foreground'    : [('disabled', self.disableFont)]}},

            'TEntry':           {'configure': { 'foreground'    : self.firstColor,
                                                'padding'       : 3,
                                                'font'          : ("Calibri", 12)}},

            'TSeparator':   {'configure': { 'padding'       : 30}}
        })

        self.theme_use('GlitchTheme')