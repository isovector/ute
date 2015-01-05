import urwid
from ute.gui import TimeEdit, Entry
from ute.model import DB, Data
from sys import argv
from time import time

class UTController:
    def __init__(self):
        self.view = UTView(self)

    def main(self):
        self.loop = urwid.MainLoop(
            self.view,
            self.view.palette,
            unhandled_input = self.view.controls
        )
        self.loop.set_alarm_in(5, self.alarm)
        self.loop.run()

    def alarm(self, _, ud):
        self.view.refresh()
        self.loop.set_alarm_in(5, self.alarm)


class UTView(urwid.WidgetWrap):
    palette = [
        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'dark red',   'bold'),
        ('screen edge',  'light blue', 'dark cyan'),
        ('main shadow',  'dark gray',  'black'),
        ('line',         'black',      'light gray', 'standout'),
        ('bg background','light gray', 'black'),
        ('bg 1',         'black',      'dark blue', 'standout'),
        ('bg 1 smooth',  'dark blue',  'black'),
        ('bg 2',         'black',      'dark cyan', 'standout'),
        ('bg 2 smooth',  'dark cyan',  'black'),
        ('button normal','light gray', 'dark blue', 'standout'),
        ('button select','white',      'dark green'),
        ('line',         'black',      'light gray', 'standout'),
        ('pg normal',    'white',      'black', 'standout'),
        ('pg complete',  'white',      'dark magenta'),
        ('pg smooth',     'dark magenta','black'),
        ('field',       'white', 'dark gray', '')
        ]

    def __init__(self, controller):
        self.controller = controller
        self.entries = urwid.SimpleListWalker([])
        urwid.WidgetWrap.__init__(self, self.main_window())

    def main_window(self):
        body = urwid.ListBox(self.entries)
        w = urwid.Pile([body])
        w = urwid.AttrMap(w, 'main shadow')

        self.refresh()

        return w

    def refresh(self):
        ids = Data.getIntervalsAfter(time() - 24 * 3600)
        toRemove = []
        for i in range(len(self.entries)):
            entry = self.entries[i]
            if entry.id == -1:
                continue

            if entry.id not in ids and entry.is_closed:
                toRemove.append(i)
            else:
                ids.remove(entry.id)

        for i in reversed(toRemove):
            self.entries[i].sync()
            self.entries.pop(i)

        for id in ids:
            self.entries.append(Entry(id))

    def controls(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        if key == "ctrl n":
            self.entries.append(Entry(-1))
            self.entries.set_focus(len(self.entries) - 1)
        if key == "ctrl e":
            self.entries.append(Entry(-1, True))
            self.entries.set_focus(len(self.entries) - 1)


def main():
    if len(argv) > 1 and argv[1] == "--install":
        DB.create()
    else:
        UTController().main()
