#!/usr/bin/env python

import urwid

palette = [
    ('normal', 'dark blue', 'dark gray'),
    ('inverse', 'dark gray', 'dark blue'),
]

def main():
    graph = urwid.BarGraph(
        ['normal', 'inverse'],
        ['normal', 'inverse'],
        { (1,0): 'normal', }, 
    )
    bardata = [(1,), (2,), (4,), (8,), (16,), (32,)]
    lines = [10, 20]
    graph.set_data(bardata, 40, lines)
    loop = urwid.MainLoop(graph, palette)
    loop.run()

if __name__ == "__main__":
    main = main()

