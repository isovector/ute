import urwid


class Catch(urwid.WidgetWrap):
    def __init__(self):
        self.widget = urwid.Edit()
        urwid.WidgetWrap.__init__(self, self.widget)

    def keypress(self, size, key):
        if key in [
                "left",
                "down",
                "up",
                "enter",
                "q",
                "Q",
                "ctrl n",
                "ctrl x",
                "ctrl e"]:
            return key
        return None

