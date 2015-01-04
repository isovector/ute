import urwid
from ute.gui import TimeEdit

class Entry(urwid.WidgetWrap):
    def __init__(self, event = False):
        self.event = event

        def wrap(w):
            return urwid.AttrMap(w, "field")

        self.type_edit = urwid.Edit()
        self.desc_edit = urwid.Edit()
        self.start_edit = TimeEdit()

        end = None
        if not event:
            self.end_edit = TimeEdit()
            end = wrap(self.end_edit)
        else:
            end = urwid.Text("event")

        self.widget = urwid.Columns(
            [
                (16, wrap(self.type_edit)),
                wrap(self.desc_edit),
                (7, wrap(self.start_edit)),
                (7, end)
            ],
            dividechars = 1)
        urwid.WidgetWrap.__init__(self, self.widget)

    @property
    def type(self):
        return self.type_edit.edit_text

    @property
    def desc(self):
        return self.desc_edit.edit_text

    @property
    def start(self):
        return self.start_edit.time

    @property
    def end(self):
        if self.event:
            return self.start
        return self.end_edit.time

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
