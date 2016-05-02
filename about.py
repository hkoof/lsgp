import urwid

import logging, prog
log = logging.getLogger(prog.name)


class AboutWindow(urwid.Padding):
    abouttext = urwid.BigText(
            '{} {}'.format(prog.name, prog.version),
            urwid.font.Thin6x6Font()
        )

    def __init__(self, *args, **kwargs):
        self.background = urwid.SolidFill('#')
        self.original_widget = urwid.Overlay(
                AboutWindow.abouttext,
                self.background,
                'center', None, 'middle', None
            ) 
        super().__init__(self.original_widget)

