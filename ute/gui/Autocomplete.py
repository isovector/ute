import urwid


class Autocomplete(urwid.WidgetWrap):
    def __init__(self):
        self.widget = urwid.Edit("")
        urwid.WidgetWrap.__init__(self, self.widget)

    def keypress(self, size, key):
        allowed = map(lambda x: str(x), range(0, 10))
