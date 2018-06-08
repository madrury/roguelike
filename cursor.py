from etc.colors import COLORS
from etc.enum import CursorTypes
from utils.utils import bresenham_line, bresenham_ray


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

    cursor_type: CursorTypes object.
      The type of election mode.  Options are PATH (draw a path from the player
      to the cursor), ADJACENT (only adjacent squares are selectable, and RAY
      (all tiles along a ray from the source through the current position of
      the cursor are highlighted).
    """
    def __init__(self, x, y, game_map, callback, *,
                 cursor_type=CursorTypes.PATH):
        self.source = (x, y)
        self.x = x
        self.y = y
        self.previous_x = None
        self.previous_y = None
        self.cursor_color = COLORS['cursor']
        self.path_color = COLORS['cursor_tail']
        self.cursor_type = cursor_type
        self.game_map = game_map
        self.callback = callback

    def move(self, dx, dy):
        self.clear()
        x, y, = self.x + dx, self.y + dy
        if self._position_valid(x, y):
            self.previous_x, self.previous_y = self.x, self.y
            self.x, self.y = x, y

    def select(self):
        self.clear()
        return self.callback.execute(self.x, self.y)

    def draw(self):
        for x, y in self._path_iter():
            if not self.game_map.fov[x, y]:
                break
            self.game_map.highlight_position(x, y, self.path_color)
        self.game_map.highlight_position(self.x, self.y, self.cursor_color)

    def clear(self):
        for x, y in self._path_iter():
            self.game_map.draw_position(x, y)

    def _position_valid(self, x, y):
        if self.cursor_type in (CursorTypes.PATH, CursorTypes.RAY):
            return self.game_map.walkable[x, y] and self.game_map.fov[x, y]
        elif self.cursor_type == CursorTypes.ADJACENT:
            return (self.game_map.walkable[x, y] 
                    and self.game_map.fov[x, y]
                    and len(self.game_map.compute_path(
                        self.source[0], self.source[1], x, y)) <= 1)
        else:
            return True

    def _path_iter(self):
        if self.cursor_type == CursorTypes.PATH:
            line = bresenham_line(self.game_map, self.source, (self.x, self.y))
            cursor_iter = iter(line)
        elif self.cursor_type == CursorTypes.ADJACENT:
            line = bresenham_line(self.game_map, self.source, (self.x, self.y))
            cursor_iter = iter(line[:1])
        elif self.cursor_type == CursorTypes.RAY:
            ray = bresenham_ray(self.game_map, self.source, (self.x, self.y))
            cursor_iter = iter(ray)
        return cursor_iter
