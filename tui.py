#!/usr/bin/env python

import collections
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
    ('bar', '', 'dark blue'),
    ('bar smooth', 'dark blue', ''),
    ('graph line background', 'brown', ''),
    ('graph line bar', 'brown', 'dark blue'),
]


class AboutWindow(urwid.Padding):
    bgchars = ('\\', '|', '/', '|')
    abouttext = urwid.BigText('{} v{}'.format('lsgp', '0.1'), urwid.font.Thin6x6Font())

    def __init__(self, *args, **kwargs):
        self.bgchar_index = len(AboutWindow.bgchars)
        self.update()
        super().__init__(self.original_widget)

    def update(self):
        self.bgchar_index += 1
        if self.bgchar_index >= len(AboutWindow.bgchars):
            self.bgchar_index = 0
        self.background = urwid.SolidFill(AboutWindow.bgchars[self.bgchar_index])
        self.original_widget = urwid.Overlay(
                AboutWindow.abouttext,
                self.background,
                'center', None, 'middle', None
            ) 


class MainWindow(urwid.Frame):
    def __init__(self):
        self.header = urwid.AttrMap(urwid.Text(('menu', "Menu")), 'header')
        self.footer = urwid.AttrMap(urwid.Text(('status', 'lsgp - LDAP Server Gauge Panel - Text mode interface to cn=monitor')), 'footer')
        self.about = AboutWindow()

        pages = [
            ('lsgp', self.about),
            ('aap', urwid.SolidFill('a')),
            ('noot', urwid.SolidFill('b')),
            ('mies', urwid.SolidFill('c')),
            ('wim', urwid.SolidFill('d')),
        ]
        self.content = NoteBook(pages)
        super().__init__(self.content, self.header, self.footer)

    def update(self, ticks):
        # call update() on all widgets
        #self.loadpage.update(ticks)
        self.about.update()


class Main:
    def __init__(self, interval=1):
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

