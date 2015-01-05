import urwid
from ute.gui import TimeEdit
from ute.model import Data
from ute.model import DB
from ute.utils import *

def wrap(w):
    return urwid.AttrMap(w, "field")

class Entry(urwid.WidgetWrap):
    _selectable = True

    def __init__(self, id = -1, event = False):
        self.event = event
        self.id = id
        self.was_focused = False
        self.is_closed = False

        defaults = (0, "", "", -1, -1)
        if id != -1:
            defaults = Data.getInterval(id)
            if defaults[3] == defaults[4]:
                event = True
            if defaults[4] != None:
                self.is_closed = True


        self.type_edit = urwid.Edit("", defaults[1])
        self.desc_edit = urwid.Edit("", defaults[2])
        self.start_edit = TimeEdit(defaults[3])
        self.end_edit = TimeEdit(defaults[4])

        end = None
        if not event and self.is_closed:
            end = wrap(self.end_edit)
        elif not self.is_closed:
            end = urwid.Text("open")
        else:
            end = urwid.Text("event")

        self.widget = urwid.Columns(
            [
                (16, wrap(self.type_edit)),
                wrap(self.desc_edit),
                (7, wrap(self.start_edit)),
                (7, end)
            ],
            dividechars = 1
        )
        urwid.WidgetWrap.__init__(self, self.widget)

    @property
    def type(self):
        return self.type_edit.edit_text

    @property
    def desc(self):
        return self.desc_edit.edit_text

    @property
    def open(self):
        return self.start_edit.time

    @property
    def close(self):
        if self.event:
            return self.open
        if not self.is_closed:
            return None
        return self.end_edit.time


    def doClose(self):
        self.sync()

        if self.is_closed:
            return

        self.end_edit.fromTimestamp(now())
        self.widget.contents[3] = (
            wrap(self.end_edit),
            self.widget.options("given", 7))

        self.is_closed = True
        Data.closeInterval(self.id, self.close)


    def keypress(self, size, key):
        if key == "ctrl x":
            self.doClose()
            return None

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

    def sync(self):
        self.id = Data.openInterval(
            self.id,
            self.type,
            self.desc,
            self.open,
            self.close
        )
        DB.commit()

    def render(self, size, focus):
        if not focus and self.was_focused:
            self.sync()
        self.was_focused = focus

        toRender = self.widget
        if focus:
            toRender = urwid.AttrMap(toRender, "header")

        return toRender.render(size, focus)
