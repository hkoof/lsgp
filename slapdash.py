#!/usr/bin/env python

import urwid


class MainWindow(urwid.Frame):
    def __init__(self):
        self.header = urwid.Text("Menu")
        self.footer = urwid.Text('"slapdash" - ldap server dashboard in text mode')
        self.tablorem = urwid.SolidFill('+')
        self.pagelorem = urwid.SolidFill('=')
        tabbox = urwid.LineBox(self.tablorem)
        pagebox = urwid.LineBox(self.pagelorem)
        columns = [ ('weight', 1, tabbox), ('weight', 4, pagebox), ]
        self.content = urwid.Columns(columns)

        super().__init__(self.content, self.header, self.footer)

def main():
    topwidget = MainWindow()
    loop = urwid.MainLoop(topwidget)
    loop.run()

if __name__ == "__main__":
    main()

