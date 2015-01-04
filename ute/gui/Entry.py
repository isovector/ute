import urwid
from ute.gui import TimeEdit

class Entry(urwid.WidgetWrap):
    def __init__(self):
        type = urwid.AttrMap(urwid.Edit(), "field")
        desc = urwid.AttrMap(urwid.Edit(), "field")
        start = urwid.AttrMap(TimeEdit(), "field")
        end = urwid.AttrMap(TimeEdit(), "field")

        self.widget = urwid.Columns(
            [(16, type), desc, (7, start), (7, end)],
            dividechars = 1)
        urwid.WidgetWrap.__init__(self, self.widget)

    def keypress(self, size, key):
        if "tab" in key:
            try:
                if "shift" in key:
                    self.widget.focus_col -= 1
                else:
                    self.widget.focus_col += 1
                return None
            except:
                pass
        return self.widget.keypress(size, key)
