import tkinter as tk
import tkinter.ttk as ttk
import configparser

class GlitchStyle(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)

    def create_theme(self, name, backgroundColor , lightBackgroundColor, fontColor , highlightsColor , darkHighlightsColor,  disableColor, disableFont, defaultFont):
        self.theme_create(themename=name, settings={
            '.':                {'configure': { 'background'    : backgroundColor ,
                                                'foreground'    : fontColor ,
                                                'highlightcolor': highlightsColor ,
                                                'font'          : defaultFont,
                                                'relief'        : 'flat'}},

            'TFrame':           {'configure': { 'relief'        : tk.FLAT,
                                                'padding'       : 10}},
            
            'TPanedwindow':     {'configure': { 'sashrelief '   : tk.SUNKEN,
                                                'background '   : 'gray10',
                                }},

            'TNotebook':        {'configure': { 'padding'       : 2}},
            
            'TNotebook.Tab':    {'configure': { 'padding'       : 2},
                                 'map'      : { 'background'    : [('selected', lightBackgroundColor)],
                                                'foreground'    : [('selected', fontColor)],
                                }},

            'TLabel':           {'configure': { 'font'          : defaultFont,
                                                'padding'       : 3,
                                                'borderwidth'   : 0,
                                                'relief'        : 'groove',
                                                'background'    : lightBackgroundColor},
                                'map'       : { 'background'    : [('disabled', disableColor)],
                                                'foreground'    : [('disabled', disableFont)],
                                                'foreground'    : [('active', darkHighlightsColor)]}},

            'TCheckbutton':     {'configure': { 'background'    : backgroundColor ,
                                                'foreground'    : fontColor ,
                                                #'indicatorcolor': fontColor ,
                                                'padding'       : 5},
                                'map'       : { 'foreground'    : [('disabled', disableFont)],
                                                'activeforeground': [('active', highlightsColor )],
                                                'indicatorcolor': [('selected', highlightsColor )],
                                                'foreground'    : [('active', darkHighlightsColor)],}},

            'TButton':          {'configure': { 'font'          : defaultFont,
                                                'background'    : lightBackgroundColor,
                                                'padding'       : 2,
                                                'borderwidth'   : 2,
                                                'justify'       : tk.CENTER,
                                                'relief'        : tk.RAISED},
                                'map'       : { 'relief'        : [('pressed', tk.SUNKEN)],
                                                'background'    : [('disabled', disableColor)],
                                                'foreground'    : [('disabled', disableFont)],
                                                #'background'    : [('active', lightBackgroundColor)],
                                                'foreground'    : [('active', darkHighlightsColor)]}},

            'TEntry':           {'configure': { 'foreground'    : backgroundColor ,
                                                'selectbackground': highlightsColor ,
                                                'padding'       : 1,
                                                'borderwidth'   : 0,
                                                'padding'       : 0,},
                                'map'       : { 'background'    : [('disabled', disableColor)],
                                                'foreground'    : [('disabled', disableFont)]}},
                                                
            'TSpinbox':         {'configure': { 'foreground'    : backgroundColor ,
                                                'selectbackground': highlightsColor ,
                                                'padding'       : 1,
                                                'borderwidth'   : 0,
                                                'arrowcolor'    : fontColor },
                                'map'       : { 'arrowcolor'    : [('active', highlightsColor )],
                                                'background'    : [('disabled', disableColor)],
                                                'foreground'    : [('disabled', disableFont)]}},

            'TScrollbar':       {'configure': { 'background'    : fontColor },
                                'map'       : { 'arrowcolor'    : [('active', highlightsColor )]}},

            'TScale':           {'configure': { 'background'    : lightBackgroundColor,
                                                'borderwidth'   : 0,
                                                'groovewidth'   : 0,
                                                'relief'        : 'flat'},
                                'map'       : { 'background '   : [('active', highlightsColor )]}},
        })
