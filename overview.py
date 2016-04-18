import urwid

import logging, prog
log = logging.getLogger(prog.name)


class Overview(urwid.Filler):
    def __init__(self, cnmonitor):
        self.cnmonitor = cnmonitor
        self.cnmonitor.subscribe(self.update, "cn=Search,cn=Operations", "monitorOpCompleted", 1)
        self.label = urwid.Text("Search operations:")
        self.searches_monitor = urwid.Text('')
        self.searches_map1 = urwid.AttrMap(self.searches_monitor, 'value')
        container1 = urwid.Pile((self.label, self.searches_map1,))
        super().__init__(container1)

    def update(self, value):
        log.debug("update value: {}".format(repr(value)))
        self.searches_monitor.set_text(str(value))

