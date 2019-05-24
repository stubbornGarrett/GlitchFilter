import tkinter as tk
import tkinter.ttk as ttk
import configparser

class GlitchStyle(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)

    def create_theme(self, name, firstColor, lightBackgroundColor, secondColor, thirdColor, disableColor, disableFont, defaultFont):
        self.theme_create(themename=name, settings={
            '.':                {'configure': { 'background'    : firstColor,
                                                'foreground'    : secondColor,
                                                'highlightcolor': thirdColor,
                                                'font'          : defaultFont,
                                                'relief'        : 'flat'}},

            'TFrame':           {'configure': { 'relief'        : tk.FLAT,
                                                'padding'       : 10}},

            'TNotebook':        {'configure': { 'padding'       : 2}},
            
            'TNotebook.Tab':    {'configure': { 'padding'       : 2}},

            'TLabel':           {'configure': { 'font'          : defaultFont,
                                                'padding'       : 3,
                                                'borderwidth'   : 2,
                                                'relief'        : 'groove',
                                                'background'    : lightBackgroundColor},
                                'map'       : { 'background'    : [('disabled', disableColor)],
                                                'foreground'    : [('disabled', disableFont)]}},

            'TCheckbutton':     {'configure': { 'background'    : firstColor,
                                                'foreground'    : secondColor,
                                                #'indicatorcolor': secondColor,
                                                'padding'       : 5},
                                'map'       : { 'foreground'    : [('disabled', disableFont)],
                                                'activeforeground': [('active', thirdColor)],
                                                'indicatorcolor': [('selected', thirdColor)]}},

            'TButton':          {'configure': { 'font'          : defaultFont,
                                                'padding'       : 2,
                                                'borderwidth'   : 3,
                                                'justify'       : tk.CENTER,
                                                'relief'        : tk.RAISED},
                                'map'       : { 'background'    : [('active', thirdColor)],
                                                'relief'        : [('pressed', tk.SUNKEN)],
                                                'background'    : [('disabled', disableColor)],
                                                'foreground'    : [('disabled', disableFont)]}},

            'TEntry':           {'configure': { 'foreground'    : firstColor,
                                                'selectbackground': thirdColor,
                                                'padding'       : 1,
                                                'borderwidth'   : 3,
                                                'padding'       : 0,}},
                                                
            'TSpinbox':         {'configure': { 'foreground'    : firstColor,
                                                'selectbackground': thirdColor,
                                                'padding'       : 1,
                                                'borderwidth'   : 2,
                                                'padding'       : 0,
                                                'arrowcolor'    : secondColor},
                                'map'       : { 'arrowcolor'    : [('active', thirdColor)]}},

            'TScrollbar':       {'configure': { 'background'    : secondColor},
                                'map'       : { 'arrowcolor'    : [('active', thirdColor)]}},

            'TScale':           {'configure': { 'background'    : lightBackgroundColor,
                                                'borderwidth'   : 1,
                                                'groovewidth'   : 1,
                                                'relief'        : 'sunken'},
                                'map'       : { 'background '   : [('active', thirdColor)]}},
        })
