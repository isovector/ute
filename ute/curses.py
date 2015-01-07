import urwid
import socket
from sys import argv, stdout
from time import time

from ute import Message
from ute.gui import TimeEdit, Entry
from ute.gui.CustomPalette import *
from ute.model import DB, Data


class UTController:
    def __init__(self):
        self.view = UTView(self)

    def main(self):
        self.loop = urwid.MainLoop(
            self.view,
            self.view.palette,
            unhandled_input = self.view.controls
        )

        self.pipe = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.pipe.bind(("localhost", 6112))
        self.loop.watch_file(self.pipe.fileno(), self.handle_pipe)

        self.loop.set_alarm_in(5, self.alarm)

        stdout.write("\x1b]2;ute: the unified tracker\x07")
        self.loop.run()

    def alarm(self, _, ud):
        self.view.refresh()
        self.loop.set_alarm_in(5, self.alarm)

    def handle_pipe(self):
        (data, _) = self.pipe.recvfrom(1024)
        msg = Message.fromJson(data)
        self.view.handle_message(msg)
        self.loop.draw_screen()


class UTView(urwid.WidgetWrap):
    palette = [
        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'dark red',   'bold'),
        ('screen edge',  'light blue', 'dark cyan'),
        ('main shadow',  'dark gray',  'black'),
        ('open',         'yellow',      '', 'bold'),
        ('field',       'white', 'dark gray', '')
        ]

    def __init__(self, controller):
        self.controller = controller
        self.entries = urwid.SimpleListWalker([])
        urwid.WidgetWrap.__init__(self, self.main_window())
        build_custom_palette()
        self.palette.extend(custom_palette)

    def main_window(self):
        body = urwid.ListBox(self.entries)
        w = urwid.Pile([body])
        w = urwid.AttrMap(w, 'main shadow')

        self.refresh()

        return w

    def refresh(self):
        for entry in self.entries:
            entry.refresh()
            if entry.is_dirty:
                entry.sync()

        ids = Data.getIntervalsAfter(time() - 6 * 3600)
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

    def handle_message(self, msg):
        if msg.action == "new":
            self.add_entry(Entry(msg = msg))

        elif msg.action == "close":
            for entry in self.entries:
                if entry.id == msg.id:
                    entry.doClose()


    def add_entry(self, entry):
        self.entries.append(entry)
        self.entries.set_focus(len(self.entries) - 1)


    def controls(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        elif key == "ctrl n":
            self.add_entry(Entry(-1))
        elif key == "ctrl e":
            self.add_entry(Entry(-1, event = True))


def main():
    if len(argv) > 1 and argv[1] == "--install":
        DB.create()
    else:
        UTController().main()
