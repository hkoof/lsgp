#!/usr/bin/env python

import urwid
from notebook import NoteBook

palette = [
    (None, '', ''),
    ('header', 'black', 'dark blue'),
    ('menu', 'light gray', 'dark blue'),
    ('footer', 'black', 'dark blue'),
    ('status', 'light gray', 'dark blue'),
    ('tab', 'dark blue', ''),
    ('tab selected', 'dark gray', 'dark blue',),
]

class MainWindow(urwid.Frame):
    def __init__(self):
        self.header = urwid.AttrMap(urwid.Text(('menu', "Menu")), 'header')
        self.footer = urwid.AttrMap(urwid.Text(('status', '"slapdash" - ldap server dashboard in text mode')), 'footer')
        pages = [
                    ('aap', urwid.SolidFill('a')),
                    ('noot', urwid.SolidFill('b')),
                    ('mies', urwid.SolidFill('c')),
                    ('wim', urwid.SolidFill('d')),
                    ('zus', urwid.SolidFill('e')),
                    ('jet', urwid.SolidFill('f')),
                    ('teun', urwid.SolidFill('g')),
                ]
        self.content = NoteBook(pages)

        super().__init__(self.content, self.header, self.footer)

def main():
    topwidget = MainWindow()
    loop = urwid.MainLoop(topwidget, palette)
    loop.run()

if __name__ == "__main__":
    main()

