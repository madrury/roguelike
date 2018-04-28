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

    game_map: tdl.Map object
      The dungeon map to select an object from.

    callback: Object with execute(x, y) method.
      An object to use as a callback once the cursor position has been
      selected.  When the user selects a position, the execute method of the
      callback is called, passing in the x, y position of the cursor.  This
      callback should return a list of turn result dictionaries to be added to
      the player turn results stack.
    """
    def __init__(self, x, y, game_map, callback):
        self.source = (x, y)
        self.x = x
        self.y = y
        self.previous_x = None
        self.previous_y = None
        self.cursor_color = COLORS['cursor']
        self.path_color = COLORS['cursor_tail']
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
        path = self.game_map.compute_path(
            self.source[0], self.source[1], self.x, self.y)
        for x, y in path[:-1]:
            self.game_map.highlight_position(x, y, self.path_color)
        self.game_map.highlight_position(self.x, self.y, self.cursor_color)

    def clear(self):
        path = self.game_map.compute_path(
            self.source[0], self.source[1], self.x, self.y)
        for x, y in path:
            self.game_map.draw_position(x, y)
