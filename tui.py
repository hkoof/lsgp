#!/usr/bin/env python

import collections
import urwid

palette = [
    (None, '', ''),
    ('header', 'black', 'dark blue'),
    ('menu', 'light gray', 'dark blue'),
    ('footer', 'black', 'dark blue'),
    ('status', 'light gray', 'dark blue'),
    ('tab', 'dark blue', ''),
    ('tab selected', 'dark gray', 'dark blue',),
    ('graph background', '', ''),
    ('bar', '', 'dark blue'),
    ('bar smooth', 'dark blue', ''),
    ('graph line background', 'brown', ''),
    ('graph line bar', 'brown', 'dark blue'),
]


class MainWindow(urwid.Frame):
    def __init__(self):
        self.header = urwid.AttrMap(urwid.Text(('menu', "Menu")), 'header')
        self.footer = urwid.AttrMap(urwid.Text(('status', 'lsgp - LDAP Server Gauge Panel - Text mode interface to cn=monitor')), 'footer')

        abouttext = urwid.BigText('lsgp', urwid.font.Thin6x6Font())
        about = urwid.Overlay(abouttext, urwid.SolidFill('/'), 'center', None, 'middle', None)
        self.about = urwid.Padding(about)
        self.loadpage = LoadPage()

        pages = [
                ('slapdash', self.about),
                ('aap', urwid.SolidFill('a')),
                ('noot', urwid.SolidFill('b')),
                ('mies', urwid.SolidFill('c')),
                ('wim', urwid.SolidFill('d')),
        ]
        self.content = NoteBook(pages)
        super().__init__(self.content, self.header, self.footer)

    def update(self, ticks):
        # call update() on all widgets
        self.loadpage.update(ticks)


class Main:
    def __init__(self, interval=2):
        self._alarm = None
        self.clockticks = 0
        self.interval = interval

        self.widget = MainWindow()
        self.loop = urwid.MainLoop(self.widget, palette)
        self.widget.update(self.clockticks)
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

