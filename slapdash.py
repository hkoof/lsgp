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
    ('graph background', '', ''),
    ('bar', '', 'dark red'),
    ('bar smooth', 'dark red', ''),
]


class LoadPage(urwid.Pile):
    def __init__(self):
        self.text = urwid.BigText('---', urwid.font.Thin6x6Font())
        textadapter = urwid.Overlay(self.text, urwid.SolidFill(), 'center', None, 'middle', None)

        self.bardata = [(v,) for v in range(10)]
        self.bargraph = urwid.BarGraph(
                ['graph background', 'bar'],
                ['graph background', 'bar'],
                {
                    (1,0): 'bar smooth',
                },
            )

        super().__init__([textadapter, self.bargraph])

    def update(self, ticks):
        self.text.set_text(str(ticks))
        self.bargraph.set_data(self.bardata, 10)

    # FIXME: implement hide and show() called by NoteBook which is to contain this as one of its widgets

class MainWindow(urwid.Frame):
    def __init__(self):
        self.header = urwid.AttrMap(urwid.Text(('menu', "Menu")), 'header')
        self.footer = urwid.AttrMap(urwid.Text(('status', '"slapdash" - ldap server dashboard in text mode')), 'footer')

        abouttext = urwid.BigText('slapdash', urwid.font.Thin6x6Font())
        about = urwid.Overlay(abouttext, urwid.SolidFill('/'), 'center', None, 'middle', None)
       
        self.loadpage = LoadPage()

        pages = [
                    ('load', urwid.Padding(self.loadpage)),
                    ('slapdash', urwid.Padding(about)),
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

    def update(self, ticks):
        # call update() on all widgets
        self.loadpage.update(ticks)

class Main:
    def __init__(self, interval=1):
        self._alarm = None
        self.clockticks = 0
        self.interval = interval

        self.widget = MainWindow()
        self.loop = urwid.MainLoop(self.widget, palette)
        self.startclock()
        self.loop.run()

    def startclock(self):
        self._alarm = self.loop.set_alarm_in(self.interval, self.clocktick)

    def stopclock(self):
        if self._alarm:
            self.loop.remove_alarm(self._alarm)
        self._alarm = None

    def clocktick(self, loop=None, data=None):
        self.clockticks += 1
        self.widget.update(self.clockticks)
        self.startclock()

if __name__ == "__main__":
    main = Main()

