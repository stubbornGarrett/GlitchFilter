import tkinter as tk
import tkinter.ttk as ttk

class GlitchStyle(ttk.Style):
    def __init__(self):
        ttk.Style.__init__(self)
        
        self.firstColor     = '#333333'
        self.secondColor    = '#eeeeee'
        self.thirdColor     = '#00aaaa'
        #self.fourthColor    = '#333333'
        self.theme_create('GlitchTheme', settings={
            '.':                {'configure': { 'background'    : self.firstColor,
                                                'foreground'    : self.secondColor,
                                                'font'          : ("Calibri", 12),
                                                'relief'        : 'flat'}},

            'TLabel':           {'configure': { 'font'          : ("Calibri", 12),
                                                'padding'       : 3,
                                                'borderwidth'   : 1,
                                                'relief'        : 'groove'}},

            'TCheckbutton':     {'configure': { 'background'    : self.firstColor,
                                                'foreground'    : self.secondColor}},

            'TButton':          {'configure': { 'font'          : ("Calibri", 12),
                                                'padding'       : 2,
                                                'borderwidth'   : 3,
                                                'justify'       : tk.CENTER,
                                                'relief'        : tk.RAISED}},

            'TEntry':           {'configure': { 'foreground'    : self.firstColor,
                                                'padding'       : 3,
                                                'font'          : ("Calibri", 12)}},

#            'TEntry.textarea':  {'configure': { 'font'          : ("Calibri", 12),
#                                                'padding'       : 3}},

            'TSeparator':   {'configure': { 'padding'       : 30}}
        })

        self.theme_use('GlitchTheme')