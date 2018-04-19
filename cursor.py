from etc.colors import COLORS


class Cursor:

    def __init__(self, x, y, map_console, game_map, callback):
        self.x = x
        self.y = y
        self.previous_x = None
        self.previous_y = None
        self.color = COLORS['yellow']
        self.map_console = map_console
        self.game_map = game_map
        self.callback = callback

    def move(self, dx, dy):
        x, y, = self.x + dx, self.y + dy
        if self.game_map.walkable[x, y] and self.game_map.fov[x, y]:
            self.previous_x, self.previous_y = self.x, self.y
            self.x, self.y = x, y

    def select(self):
        return self.callback(self.x, self.y)

    def draw(self):
        if self.previous_x and self.previous_y:
            self.map_console.draw_char(
                self.previous_x, self.previous_y, ' ',
                fg=None, bg=COLORS['light_ground'])
        self.map_console.draw_char(
            self.x, self.y, ' ', fg=None, bg=self.color)
