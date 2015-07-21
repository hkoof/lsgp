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

    def update(self, txt):
        self.text.set_text(txt)

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
                    ('ldappa', self.about),
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

    def update(self, ticks, time):
        self.timepage.update(time.strftime("%H:%M:%S"))


class Ticker():
    def __init__(self, loop, callback):
        self._loop = loop
        self._callback = callback

        self.running = False
        self.ticks = 0

    def start(self):
        # loopclock != wallclock and wwe want the ticks to occur every
        # wallclock minute. Using sleep(60) everythime may skew to the
        # point of skipping a wallclock minute, since things may be done
        # meanwhile in the same thread in the event loop.
        #
        # So we try to start just after the current minute will begin,
        # and schedule every next ticker call at current loop-time + 60.
        #
        looptime = self._loop.time()
        clocktime = time.time()

        secs2start = 60 - int(clocktime) % 60
        log.debug("starting ticker in {} seconds".format(secs2start))

        self._loop.call_at(looptime + secs2start, self.tick)
        self.running = True

    def stop(self):
        self.running = False

    def tick(self):
        looptime = self._loop.time()
        clocktime = datetime.datetime.now()
        if not self.running:
            return
        self.ticks += 1
        self._loop.call_soon(self._callback, self.ticks, clocktime)
        self._loop.call_at(looptime + 60, self.tick)


class MainLoop(urwid.MainLoop):
    # Workaround to leave terminal usable after exception (eg. ctrl-c)
    # (thanks "regebro", in urwid's github issue #126)
    def run(self):
        try:
            self._run()
        except urwid.ExitMainLoop:
            pass
        except BaseException:
            self.screen.stop()
            raise

def main():
    eventloop = asyncio.get_event_loop()
    widget = MainWindow()
    ticker = Ticker(eventloop, widget.update)
    ticker.start()

    mainloop = MainLoop(
        widget,
        palette,
        unhandled_input=handleInput,
        event_loop=urwid.AsyncioEventLoop(loop=eventloop),
        )
    mainloop.run()

    # FIXME: not needed(?)
    ticker.stop()
    event_loop.stop()
    event_loop.close()


def handleInput(key):
    if key == 'esc':
        raise urwid.ExitMainLoop()


if __name__ == "__main__":
    main()

