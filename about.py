import urwid

import logging, prog
log = logging.getLogger(prog.name)


class AboutWindow(urwid.Padding):
    bgchars = ('\\', '|', '/', '|')
    abouttext = urwid.BigText(
            '{} {}'.format(prog.name, prog.version),
            urwid.font.Thin6x6Font()
        )

    def __init__(self, *args, **kwargs):
        self.active = True
        self.bgchar_index = len(AboutWindow.bgchars)
        self.update()
        super().__init__(self.original_widget)

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def update(self):
        if not self.active:
            return
        self.bgchar_index += 1
        if self.bgchar_index >= len(AboutWindow.bgchars):
            self.bgchar_index = 0
        self.background = urwid.SolidFill(AboutWindow.bgchars[self.bgchar_index])
        self.original_widget = urwid.Overlay(
                AboutWindow.abouttext,
                self.background,
                'center', None, 'middle', None
            ) 


