import logging

import urwid

import prog

log = logging.getLogger(prog.name)

class Overview(urwid.Filler):
    def __init__(self):
        self.connections_label = urwid.Text("Connections:")
        # self.connections_monitor = urwid.Text('', align='right')
        self.connections_monitor = urwid.Text('---')
        self.connections_map1 = urwid.AttrMap(self.connections_monitor, 'value')
        container1 = urwid.Pile((self.connections_label, self.connections_map1,))
        super().__init__(container1)

    def update(self, value):
        self.connections_monitor.set_text(value)

