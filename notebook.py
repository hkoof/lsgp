import urwid

class NoteBook(urwid.Columns):
    '''pages : list of tuples like ('label', widget)'''
    def __init__(self, pages):
        self.tabs = list()
        self.pages = list()
        for p in pages:
            widget = p[1]
            self.pages.append(widget)
            button = urwid.Button(p[0], self.activatePage, widget)
            tab = urwid.AttrMap(button, 'tab', focus_map='tab selected')
            self.tabs.append(tab)
        
        buttonlist = urwid.SimpleFocusListWalker(self.tabs)
        tabbox = urwid.ListBox(buttonlist)
        self.pagebox = urwid.WidgetPlaceholder(self.pages[0])

        columns = [
            ('weight', 1, urwid.LineBox(tabbox)),
            ('weight', 5, urwid.LineBox(self.pagebox)),
        ]
        super().__init__(columns)
        self.activatePage(self.tabs[0], self.pages[0])


    def activatePage(self, button, widget):
        for page in self.pages:
            if page == widget:
                continue
            if hasattr(page, 'deactivate'):
                page.deactivate()

        if hasattr(widget, 'activate'):
            widget.activate() 

        self.pagebox.original_widget = widget

