import urwid

import logging, prog
log = logging.getLogger(prog.name)


class Overview(urwid.Filler):
    def __init__(self, cnmonitor):
        self.cnmonitor = cnmonitor
        self.cnmonitor.subscribe(self.update, "cn=Search,cn=Operations", "monitorOpCompleted", 5)
        self.connections_label = urwid.Text("Connections:")
        # self.connections_monitor = urwid.Text('', align='right')
        self.connections_monitor = urwid.Text('---')
        self.connections_map1 = urwid.AttrMap(self.connections_monitor, 'value')
        container1 = urwid.Pile((self.connections_label, self.connections_map1,))
        super().__init__(container1)

    def update(self, value):
        log.debug("update value: {}".format(repr(value)))
        self.connections_monitor.set_text(str(value))

