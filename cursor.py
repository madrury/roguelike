from etc.colors import COLORS


class Cursor:
    """Represents a freely movable cursor the player can use to select
    individual entities in the dungeon.

    This is used in a special game state, GameStates.CURSOR_INPUT.

    Attributes
    ----------

    x: int
      The x position of the cursor.

    y: int
      The y position of the cursor.

    previous_x: int
      The previous x position of the cursor.

    previous_y: int
      The previous y position of the cursor.

    color: tuple of RGB values
      The color of the cursor.

    map_console: tdl.Console object
      The console to draw the cursor onto.

    game_map: tdl.Map object
      The dungeon map to select an object from.

    callback: Object with execute(x, y) method.
      An object to use as a callback once the cursor position has been
      selected.  When the user selects a position, the execute method of the
      callback is called, passing in the x, y position of the cursor.  This
      callback should return a list of turn result dictionaries to be added to
      the player turn results stack.
    """
    def __init__(self, x, y, map_console, game_map, callback):
        self.source = (x, y)
        self.x = x
        self.y = y
        self.previous_x = None
        self.previous_y = None
        self.color = COLORS['cursor']
        self.path_color = COLORS['cursor_tail']
        self.map_console = map_console
        self.game_map = game_map
        self.callback = callback

    def move(self, dx, dy):
        self.clear()
        x, y, = self.x + dx, self.y + dy
        if self.game_map.walkable[x, y] and self.game_map.fov[x, y]:
            self.previous_x, self.previous_y = self.x, self.y
            self.x, self.y = x, y

    def select(self):
        self.clear()
        return self.callback.execute(self.x, self.y)

    def draw(self):
        self._draw_path(self.path_color, self.color)

    def clear(self):
        self._draw_path(COLORS['light_ground'], COLORS['light_ground'])

    def _draw_path(self, path_color, cursor_color):
        path = self.game_map.compute_path(
            self.source[0], self.source[1], self.x, self.y)
        for x, y in path[:-1]:
            self.map_console.draw_char(x, y, ' ', fg=None, bg=path_color)
        self.map_console.draw_char(
            self.x, self.y, ' ', fg=None, bg=cursor_color)


