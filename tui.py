#!/usr/bin/env python

import collections
import urwid

from notebook import NoteBook
from about import AboutWindow
from overview import Overview

import logging, prog
log = logging.getLogger(prog.name)

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
    ('value', 'light red', 'white'),
]


class MainWindow(urwid.Frame):
    def __init__(self):
        self.header = urwid.AttrMap(urwid.Text(('menu', "Menu")), 'header')
        self.footer = urwid.AttrMap(urwid.Text(('status', 'lsgp - LDAP Server Gauge Panel - Text mode interface to cn=monitor')), 'footer')

        self.overview = Overview()
        self.about = AboutWindow()

        pages = [
            ('lsgp', self.about),
            ('Overview', self.overview),
            ('aap', urwid.SolidFill('a')),
            ('noot', urwid.SolidFill('b')),
            ('mies', urwid.SolidFill('c')),
            ('wim', urwid.SolidFill('d')),
        ]
        self.content = NoteBook(pages)
        super().__init__(self.content, self.header, self.footer)

    def update(self, ticks):
        # call update() on all widgets
        self.about.update()

    def receive_number_connections(self, result):
        number_connections = result[0]['monitorCounter'][0]
        log.debug("ldap result: " + str(number_connections))
        self.overview.update(str(number_connections))


class Main:
    def __init__(self, cnmonitor, interval=1):
        self.cnmonitor = cnmonitor
        self._alarm = None
        self.clockticks = 0
        self.interval = interval

        self.widget = MainWindow()
        self.loop = urwid.MainLoop(self.widget, palette)

    def run(self):
        self.loop.watch_file(self.cnmonitor.fileno(), self.cnmonitor.poll)
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
        self.cnmonitor.search(
                "cn=Current,cn=Connections,cn=Monitor",
                0, '', ['+'],
                self.widget.receive_number_connections,
            )
        self.startclock()
