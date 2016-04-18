#!/usr/bin/env python

import collections
import time
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
    def __init__(self, cnmonitor, interval=1):
        self.cnmonitor = cnmonitor
        self.interval = interval
        self._lasttime = None
        self._alarm = None
        self.clockticks = 0

        self.loop = urwid.MainLoop(self, palette)
        self.header = urwid.AttrMap(urwid.Text(('menu', "Menu")), 'header')
        self.footer = urwid.AttrMap(urwid.Text(('status', 'lsgp - LDAP Server Gauge Panel - Text mode interface to cn=monitor')), 'footer')

        self.overview = Overview(self.cnmonitor)
        self.about = AboutWindow()

        pages = [
            ('Overview', self.overview),
            ('lsgp', self.about),
            ('aap', urwid.SolidFill('a')),
            ('noot', urwid.SolidFill('b')),
            ('mies', urwid.SolidFill('c')),
            ('wim', urwid.SolidFill('d')),
        ]
        self.content = NoteBook(pages)
        super().__init__(self.content, self.header, self.footer)

    def run(self):
        self.loop.watch_file(self.cnmonitor.fileno(), self.cnmonitor.poll)
        self.startclock()
        self.loop.run()

    def startclock(self):
        self._alarm = self.loop.set_alarm_in(.01, self.clocktick)

    def stopclock(self):
        if self._alarm:
            self.loop.remove_alarm(self._alarm)
        self._alarm = None

    def clocktick(self, *args):
        log.debug("clocktick args: {}".format(repr(args)))
        self.cnmonitor.update(self.clockticks)
        self.clockticks += 1

        # Try correct time lost in running code
        now = time.time()
        if not self._lasttime:
            interval = self.interval
        else:
            interval = self.interval - (now - self._lasttime - self.interval)
        self._lasttime = now
        log.debug("time: corrected alarm time interval: {}".format(interval))

        # Schedule next clock tick in the event loop
        self._alarm = self.loop.set_alarm_in(interval, self.clocktick)
