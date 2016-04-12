import urwid
import prog

class AboutWindow(urwid.Padding):
    bgchars = ('\\', '|', '/', '|')
    abouttext = urwid.BigText(
            '{} {}'.format(prog.name, prog.version),
            urwid.font.Thin6x6Font()
        )

    def __init__(self, *args, **kwargs):
        self.bgchar_index = len(AboutWindow.bgchars)
        self.update()
        super().__init__(self.original_widget)

    def update(self):
        self.bgchar_index += 1
        if self.bgchar_index >= len(AboutWindow.bgchars):
            self.bgchar_index = 0
        self.background = urwid.SolidFill(AboutWindow.bgchars[self.bgchar_index])
        self.original_widget = urwid.Overlay(
                AboutWindow.abouttext,
                self.background,
                'center', None, 'middle', None
            ) 


