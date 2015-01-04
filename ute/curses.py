import urwid
from ute.gui import TimeEdit, Entry

class UTController:
    def __init__(self):
        self.view = UTView(self)

    def main(self):
        self.loop = urwid.MainLoop(
            self.view,
            self.view.palette,
            unhandled_input = self.view.controls
        )
        self.loop.run()


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
        self.started = True
        self.start_time = None
        self.offset = 0
        self.last_offset = None
        self.entries = urwid.SimpleListWalker([])
        urwid.WidgetWrap.__init__(self, self.main_window())

    def menu(self, title, choices, onSelect):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', onSelect, c)
            body.append(urwid.AttrMap(button, None, focus_map='header'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def main_window(self):
        body = urwid.ListBox(self.entries)
        w = urwid.Pile([body])
        w = urwid.AttrMap(w, 'main shadow')
        return w

    def controls(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()
        if key == "ctrl n":
            self.entries.append(Entry())
            self.entries.set_focus(len(self.entries) - 1)


def main():
    UTController().main()
