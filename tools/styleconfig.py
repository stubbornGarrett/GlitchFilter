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

        self.defaultFont        = ("Calibri", 12)

        self.theme_create('GlitchTheme', settings={
            '.':                {'configure': { 'background'    : self.firstColor,
                                                'foreground'    : self.secondColor,
                                                'highlightcolor': self.thirdColor,
                                                'font'          : self.defaultFont,
                                                'relief'        : 'flat'}},

            'TFrame':           {'configure': { 'relief'        : tk.FLAT,
                                                'padding'       : 10}},

            'TNotebook':        {'configure': { 'padding'       : 2}},
            
            'TNotebook.Tab':    {'configure': { 'padding'       : 2}},

            'TLabel':           {'configure': { 'font'          : self.defaultFont,
                                                'padding'       : 3,
                                                'borderwidth'   : 1,
                                                'relief'        : 'groove'},
                                'map'       : { 'background'    : [('disabled', self.disableColor)],
                                                'foreground'    : [('disabled', self.disableFont)]}},

            'TCheckbutton':     {'configure': { 'background'    : self.firstColor,
                                                'foreground'    : self.secondColor,
                                                #'indicatorcolor': self.secondColor,
                                                'padding'       : 5},
                                'map'       : { 'foreground'    : [('disabled', self.disableFont)],
                                                'activeforeground': [('active', self.thirdColor)],
                                                'indicatorcolor': [('selected', self.thirdColor)]}},

            'TButton':          {'configure': { 'font'          : self.defaultFont,
                                                'padding'       : 2,
                                                'borderwidth'   : 3,
                                                'justify'       : tk.CENTER,
                                                'relief'        : tk.RAISED},
                                'map'       : { 'background'    : [('active', self.thirdColor)],
                                                'relief'        : [('pressed', tk.SUNKEN)],
                                                'background'    : [('disabled', self.disableColor)],
                                                'foreground'    : [('disabled', self.disableFont)]}},

            'TEntry':           {'configure': { 'foreground'    : self.firstColor,
                                                'selectbackground': self.thirdColor,
                                                'padding'       : 1,
                                                'borderwidth'   : 3,
                                                'padding'       : 0,}},

            'TScrollbar':       {'configure': { 'background'    : self.secondColor},
                                'map'       : { 'arrowcolor'    : [('active', self.thirdColor)]}},

            'TSeparator':       {'configure': { 'padding'       : 30}}
        })

        self.theme_use('GlitchTheme')