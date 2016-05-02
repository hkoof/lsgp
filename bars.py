#!/usr/bin/env python

import urwid

palette = [
    ('normal', 'dark blue', 'dark gray'),
    ('inverse', 'dark gray', 'dark blue'),
    ('other', 'dark gray', 'light blue'),
    ('other2', 'light blue', 'dark blue'),
    ('other3', 'light blue', 'dark gray'),
]

def main():
    graph = urwid.BarGraph(
        ['normal', 'inverse', 'other'],
        ['normal', 'inverse', 'other'],
        {
           (1,0): 'normal',
           (2,0): 'other3',
           (2,1): 'other2',
        }, 
    )
    bardata = [(1,6), (2,5), (4,4), (8,3), (16,2), (32,1)]
    ## exposes bug in bar 4? ## bardata = [(1,1), (2,2), (4,3), (8,4), (16,5), (32,6)]
    lines = [3.5, 20]
    graph.set_data(bardata, 40, lines)
    loop = urwid.MainLoop(graph, palette)
    loop.run()

if __name__ == "__main__":
    main = main()

