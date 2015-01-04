import urwid

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
        ('pg smooth',     'dark magenta','black')
        ]

    def __init__(self, controller):
        self.controller = controller
        self.started = True
        self.start_time = None
        self.offset = 0
        self.last_offset = None
        urwid.WidgetWrap.__init__(self, self.main_window())

    def menu(self, title, choices, onSelect):
        body = [urwid.Text(title), urwid.Divider()]
        for c in choices:
            button = urwid.Button(c)
            urwid.connect_signal(button, 'click', onSelect, c)
            body.append(urwid.AttrMap(button, None, focus_map='header'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

    def main_window(self):
        body = self.menu("Hello", ["a", "b"], lambda c, u: 1)
        body = urwid.BoxAdapter(body, 5)
        body = urwid.LineBox(body)
        dates = self.menu("Hello", ["a", "b"], lambda c, u: 1)
        dates = TimeEdit()
#        dates = urwid.BoxAdapter(dates, 5)
        dates = urwid.LineBox(dates)
        w = urwid.Columns([(32, dates), body], 1)
        w = urwid.Filler(w)
        w = urwid.AttrMap(w, 'main shadow')
        return w

    def controls(self, key):
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()


class TimeEdit(urwid.WidgetWrap):
    def __init__(self):
        self.edit = urwid.Edit("", "12:34")
        urwid.WidgetWrap.__init__(self, self.edit)

    def render(self, size, focus):
        if self.edit.edit_pos > 4:
            self.edit.edit_pos = 4

        toRender = self.edit
        if focus:
            toRender = urwid.AttrMap(toRender, "header")
        result = toRender.render(size, focus)
        return result

    def keypress(self, size, key):
        allowed = map(lambda x: str(x), range(0, 10))

        handled = []
        handled.extend(allowed)
        handled.extend(["left", "right", "delete", "backspace"])

        if key not in handled:
            return key

        if key in allowed:
            self.edit.keypress(size, "delete")

        result = self.edit.keypress(size, key)

        self.validate()

        if self.edit.edit_pos == 2:
            if key in ["left", "backspace"]:
                self.edit.edit_pos -= 1
            else:
                self.edit.edit_pos += 1
        if self.edit.edit_pos > 4:
            return "right"
        return result

    def mouse_event(self, size, event, button, x, y, focus):
        result = self.edit.mouse_event(size, event, button, x, y, focus)
        if self.pos == 2:
            self.pos = 3
        return result

    @property
    def text(self):
        return self.edit.edit_text

    @text.setter
    def text(self, value):
        self.edit.edit_text = value

    @property
    def pos(self):
        return self.edit.edit_pos

    @pos.setter
    def pos(self, value):
        self.edit.edit_pos = value

    def validate(self):
        def clamp(val, bot, top):
            return max(bot, min(val, top))

        h = int(self.text[0:2])
        m = int(self.text[3:5])
        if not (0 < h and h < 24 and 0 < m and m < 60):
            h = clamp(h, 0, 23)
            m = clamp(m, 0, 59)
            self.text = '{:0^2}:{:0^2}'.format(h, m)


def main():
    UTController().main()
