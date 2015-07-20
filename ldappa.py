#!/usr/bin/env python

import logging
log = logging.getLogger('hko')
log.setLevel(logging.DEBUG)
log.addHandler(logging.FileHandler("/tmp/log"))

import asyncio
import time, datetime
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


class TimePage(urwid.Pile):
    def __init__(self):
        self.hidden = True
        self.text = urwid.BigText('---', urwid.font.Thin6x6Font())
        textfit = urwid.Overlay(self.text, urwid.SolidFill(), 'center', None, 'middle', None)
        super().__init__([(10, textfit), urwid.SolidFill('='), urwid.SolidFill('-'),])

    def activate(self):
        self.hidden = False

    def deactivate(self):
        self.hidden = True

    def update(self, ticks):
        if self.hidden:
            return
        self.text.set_text("QQleQ")

    def updategraph(self):
        # hlines = [1,2]
        self.bargraph.set_data(list(self.bardata), self.bartop)


class MainWindow(urwid.Frame):
    def __init__(self):
        self.header = urwid.AttrMap(urwid.Text(('menu', "Menu")), 'header')
        self.footer = urwid.AttrMap(urwid.Text(('status', '"Ldappa" - ldap text mode tool')), 'footer')

        abouttext = urwid.BigText('Ldappa', urwid.font.Thin6x6Font())
        about = urwid.Overlay(abouttext, urwid.SolidFill('/'), 'center', None, 'middle', None)
        self.about = urwid.Padding(about)
        self.timepage = TimePage()

        pages = [
                    ('time', self.timepage),
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


def clocktick(widget, loop):
    loop_epoch_secs = loop.time()
    clock_epoch_secs = time.time()

    looptime = datetime.datetime.fromtimestamp(loop_epoch_secs)
    clocktime = datetime.datetime.fromtimestamp(clock_epoch_secs)

    log.debug("Loop secs:  {}    Loop time:  {}".format(loop_epoch_secs, looptime))
    log.debug("Clock secs: {}    Clock time: {}".format(clock_epoch_secs, clocktime))

    # Call again (and again, and ...) 1 minute later
    loop.call_at(loop_epoch_secs + 60, clocktick, widget, loop)
    #loop.call_later(60, clocktick, widget, loop)
    log.debug("---")


def handleInput(key):
    if key == 'esc':
        raise urwid.ExitMainLoop()


def main():
    eventloop = asyncio.get_event_loop()
    widget = MainWindow()
    eventloop.call_soon(clocktick ,widget, eventloop)

    mainloop = urwid.MainLoop(
        widget,
        palette,
        unhandled_input=handleInput,
        event_loop=urwid.AsyncioEventLoop(loop=eventloop),
        )
    mainloop.run()
    event_loop.close()

if __name__ == "__main__":
    main()

