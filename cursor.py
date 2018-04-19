from etc.colors import COLORS


class Cursor:

    def __init__(self, x, y, map_console, callback):
        self.x = x
        self.y = y
        self.color = COLORS['yellow']
        self.map_console = map_console
        self.callback = callback

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def select(self):
        return self.callback(self.x, self.y)

    def draw(self):
        self.map_console.draw_char(
            self.x, self.y, ' ', fg=None, bg=self.color)
