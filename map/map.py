import numpy as np
from itertools import product
from random import randint, choice

from tdl.map import Map

from etc.colors import COLORS
from colors import random_light_water, random_dark_water


class GameMap(Map):
    """Represents the game map for a dungeon floor.

    The GameMap object is the main place that information on the current
    dungeon map is located.  It contains information on the layout of the
    dungeon, the various types of tiles, and the way the tiles are rendered.
    Most introspection of the current game state is facilitated by a GameMap
    object.

    Parameters
    ----------
    floor: DungeonFloor object
      The built out dungeon floor object to use in constructing the GameMap.

    console: tdl.Console object
      The console to draw the dungeon floor on.

    Attributes on Parent
    --------------------
    walkable: np.array of bool
      Is the tile able to be walked on? This is used to define walls in the
      dungeon.

    transparant: np.array of bool
      Does the tile block fov?

    fov: np.array of bool
      Is the tile in the player's current fov?

    Attributes
    ----------
    explored: np.array of bool
      Has the tile in this location been explored?

    pool: np.array of bool
      Does the tile currently hold a pool of water?

    fg_colors: ColorArray object
      The RGB colors currently rendered in the foreground of each tile

    bg_colors: ColorArray object
      The RGB colors currently rendered in the background of each tile

    chars: np.array of strings
      The character currently rendered in each tile.
    """
    def __init__(self, floor, console):
        width, height = floor.width, floor.height
        super().__init__(width, height)
        self.floor = floor
        self.console = console
        self.explored = np.zeros((width, height)).astype(bool)
        self.pool = np.zeros((width, height)).astype(bool)
        self.fg_colors = ColorArray((width, height))
        self.bg_colors = ColorArray((width, height))
        self.chars = np.full((width, height), ' ')
        self.blit_floor()

    def blit_floor(self):
        for room in self.floor.rooms:
            for x, y in room:
                self.make_transparent_and_walkable(x, y)
        for tunnel in self.floor.tunnels:
            for x, y in tunnel:
                self.make_transparent_and_walkable(x, y)
        for pool in self.floor.pools:
            pool.write_to_game_map(self)

    def place_player(self, player):
        placed = False
        while not placed:
            start_room = choice(self.floor.rooms)
            x, y = start_room.random_point()
            if not self.pool[x, y]:
                player.x, player.y = x, y
                placed = True

    def draw_entity(self, entity):
        bg = self.bg_colors[entity.x, entity.y]
        if self.fov[entity.x, entity.y]:
            self.draw_char(entity.x, entity.y, entity.char, 
                        fg=entity.color, bg=bg)

    def update_entity(self, entity):
        bg = self.bg_colors[entity.x, entity.y]
        self.update_position(entity.x, entity.y, entity.char,
                             fg=entity.color, bg=bg)

    def update_and_draw_entity(self, entity):
        self.update_entity(entity)
        self.draw_entity(entity)

    def undraw_entity(self, entity):
        self.draw_blank(entity.x, entity.y)

    def remove_entity(self, entity):
        self.fg_colors[entity.x, entity.y] = None
        self.chars[entity.x, entity.y] = ' '

    def remove_and_undraw_entity(self, entity):
        self.remove_entity(entity)
        self.undraw_entity(entity)

    def draw_blank(self, x, y):
        bg = self.bg_colors[x, y]
        self.draw_char(x, y, ' ', fg=None, bg=bg)

    def update_position(self, x, y, char, fg=None, bg=None):
        self.fg_colors[x, y] = fg
        self.bg_colors[x, y] = bg
        self.chars[x, y] = char

    def draw_char(self, x, y, char, fg=None, bg=None):
        self.console.draw_char(x, y, char, fg, bg)

    def highlight_position(self, x, y, color):
        char = self.chars[x, y]
        fg = self.fg_colors[x, y]
        self.draw_char(x, y, char, fg=fg, bg=color)

    def draw_position(self, x, y):
        char = self.chars[x, y]
        fg = self.fg_colors[x, y]
        bg = self.bg_colors[x, y]
        self.draw_char(x, y, char, fg=fg, bg=bg)

    def update_and_draw_char(self, x, y, char, fg=None, bg=None):
        self.update_position(x, y, char, fg, bg)
        self.console.draw_char(x, y, char, fg, bg)

    def update_and_draw_all(self, entities, fov_recompute=True):
        if fov_recompute:
            self.update_and_draw_layout() 
        entities_in_render_order = sorted(
            entities, key=lambda x: x.render_order.value)
        for entity in entities_in_render_order:
            self.update_and_draw_entity(entity)

    def undraw_all(self, entities):
        for entity in entities:
            self.undraw_entity(entity)

    def update_and_draw_layout(self):
        for x, y in self:
            wall = not self.transparent[x, y]
            pool = self.pool[x, y]
            if self.fov[x, y]:
                if wall:
                    self.update_and_draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('light_wall'))
                elif pool:
                    self.update_and_draw_char(
                        x, y, '~', 
                        fg=random_light_water(), bg=random_light_water())
                else:
                    self.update_and_draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('light_ground'))
                self.explored[x, y] = True
            elif self.explored[x, y]:
                if wall:
                    self.update_and_draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('dark_wall'))
                elif pool:
                    self.update_and_draw_char(
                        x, y, '~', 
                        fg=random_dark_water(), bg=random_dark_water())
                else:
                    self.update_and_draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('dark_ground'))

    def within_bounds(self, x, y):
        return (0 <= x < self.width) and (0 <= y < self.height)

    def make_transparent_and_walkable(self, x, y):
        self.walkable[x, y] = True
        self.transparent[x, y] = True


class ColorArray:
    """A two by two array of RGB tuples."""
    def __init__(self, shape):
        # This needs to be an array of floating points so that we
        # can store NaNs.
        self.a = np.zeros((shape[0], shape[1], 3))

    def __getitem__(self, idxs):
        if len(idxs) == 2:
            colors = self.a[idxs[0], idxs[1], :]
            if np.all(np.isnan(colors)):
                return None
            else:
                return tuple(colors.astype(int))
        else:
            return self.a[idxs]

    def __setitem__(self, idxs, value):
        if len(idxs) == 2:
            self.a[idxs[0], idxs[1], :] = value
        else:
            self.a[idxs] = value
