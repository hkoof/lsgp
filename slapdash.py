#!/usr/bin/env python

import urwid

palette = [
        ('header', 'black', 'dark blue'),
        ('menu', 'light gray', 'dark blue'),
        ('footer', 'black', 'dark blue'),
        ('status', 'light gray', 'dark blue'),
        ('linebox', 'dark blue', 'black'),
        ]

class MainWindow(urwid.Frame):
    def __init__(self):
        self.header = urwid.AttrMap(urwid.Text(('menu', "Menu")), 'header')
        self.footer = urwid.AttrMap(urwid.Text(('status', '"slapdash" - ldap server dashboard in text mode')), 'footer')
        self.tablorem = urwid.SolidFill('+')
        self.pagelorem = urwid.SolidFill('=')
        tabbox = urwid.AttrMap(urwid.LineBox(self.tablorem), 'linebox')
        pagebox = urwid.LineBox(self.pagelorem)
        columns = [ ('weight', 1, tabbox), ('weight', 4, pagebox), ]
        self.content = urwid.Columns(columns)

        super().__init__(self.content, self.header, self.footer)

def main():
    topwidget = MainWindow()
    loop = urwid.MainLoop(topwidget, palette)
    loop.run()

if __name__ == "__main__":
    main()

