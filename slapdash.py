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


class LoadPage(urwid.Pile):
    def __init__(self):
        self.hidden = True
        self.procfd = open("/proc/loadavg")
        self.text = urwid.BigText('---', urwid.font.Thin6x6Font())
        textadapter = urwid.Overlay(self.text, urwid.SolidFill(), 'center', None, 'middle', None)

        self.nbars = 60
        self.bartop = 3
        self.bardata = collections.deque([(0,) for tmp in range(self.nbars)], self.nbars)
        self.bargraph = urwid.BarGraph(
                ['graph background', 'bar'],
                ['graph line background', 'graph line bar'],
                { (1,0): 'bar smooth', },
            )
        self.bargraph.set_bar_width(1)

        super().__init__([(10, textadapter), self.bargraph,])

    def activate(self):
        self.hidden = False
        self.updategraph()

    def deactivate(self):
        self.hidden = True

    def update(self, ticks):
        if self.hidden:
            return
        loadline = self.procfd.readline(128)
        self.procfd.seek(0)
        load1m = loadline.split()[0]
        load1number = float(load1m)
        self.text.set_text(load1m)
        self.bardata.append((load1number,))
        self.updategraph()

    def updategraph(self):
        hlines = [1,2]
        self.bargraph.set_data(list(self.bardata), self.bartop, hlines)


class MainWindow(urwid.Frame):
    def __init__(self):
        self.header = urwid.AttrMap(urwid.Text(('menu', "Menu")), 'header')
        self.footer = urwid.AttrMap(urwid.Text(('status', '"slapdash" - ldap server dashboard in text mode')), 'footer')

        abouttext = urwid.BigText('slapdash', urwid.font.Thin6x6Font())
        about = urwid.Overlay(abouttext, urwid.SolidFill('/'), 'center', None, 'middle', None)
        self.about = urwid.Padding(about)
        self.loadpage = LoadPage()

        pages = [
                    ('load', self.loadpage),
                    ('slapdash', self.about),
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

