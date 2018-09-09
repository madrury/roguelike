import numpy as np
from itertools import product
from random import randint, choice

from tdl.map import Map

from entity_list import EntityList
from etc.colors import COLORS


class GameMap(Map):
    """Represents the game map for a dungeon floor.

    The GameMap object is the main place that information on the current
    dungeon map is located.  It contains information on the layout of the
    dungeon, the various types of tiles, and the way the tiles are rendered.
    Most introspection of the current game state is facilitated by a GameMap
    object.

    # TODO: Discuss which each of the types of methods (update, draw, etc)
    # means.

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

    transparent: np.array of bool
      Does the tile block fov?

    fov: np.array of bool
      Is the tile in the player's current fov?

    Attributes
    ----------
    explored: np.array of bool
      Has the tile in this location been explored?

    water: np.array of bool
      Does the tile currently hold a water?

    fire: np.array of bool
      Is the tile currently on fire?

    door: np.array of bool:
        Does the tile currently contiain a door?

    shrub: np.array of bool
      Does the tile currently contain a shrub?

    steam: np.array of bool
      Does he tile currently contain steam?

    blocked: np.array of bool
      Is there currently a blocking entity in this spot?

    terrain: np.array of bool
      Does the tile currently hold any premenant terrain?

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
        self.entities = EntityList(width, height)
        # TODO: Add to docstring
        self.upward_stairs_position = None
        self.downward_stairs_position = None
        # These need to be int8's to work with the tcod pathfinder
        self.explored = np.zeros((width, height), dtype=np.int8)
        self.illuminated = np.zeros((width, height), dtype=np.int8)
        self.water = np.zeros((width, height), dtype=np.int8)
        self.ice = np.zeros((width, height), dtype=np.int8)
        self.fire = np.zeros((width, height), dtype=np.int8)
        self.door = np.zeros((width, height), dtype=np.int8)
        self.shrub = np.zeros((width, height), dtype=np.int8)
        self.steam = np.zeros((width, height), dtype=np.int8)
        self.terrain = np.zeros((width, height), dtype=np.int8)
        self.blocked = np.zeros((width, height), dtype=np.int8)
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
        for entity in self.floor.objects:
            entity.commitable.commit(self)

    def update_entity(self, entity):
        if self.visible(entity.x, entity.y):
            entity.seen = True
            bg = (entity.bg_color if entity.bg_color
                  else self.bg_colors[entity.x, entity.y])
            self.update_position(entity.x, entity.y, entity.char,
                                 fg=entity.fg_color, bg=bg)
        elif (entity.visible_out_of_fov and entity.seen):
            bg = (entity.dark_bg_color if entity.dark_bg_color
                  else self.bg_colors[entity.x, entity.y])
            self.update_position(entity.x, entity.y, entity.char,
                                 fg=entity.dark_fg_color, bg=bg)

    def draw_entity(self, entity):
        if self.visible(entity.x, entity.y):
            self.draw_char(entity.x, entity.y, entity.char,
                           fg=entity.fg_color, bg=entity.bg_color)
        elif (entity.visible_out_of_fov and entity.seen):
            self.draw_char(entity.x, entity.y, entity.char,
                           fg=entity.dark_fg_color, bg=entity.dark_bg_color)

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

    def update_and_draw_all(self):
        self.update_and_draw_layout()
        entities_in_render_order = sorted(
            self.entities, key=lambda x: x.render_order.value)
        for entity in entities_in_render_order:
            self.update_and_draw_entity(entity)

    def undraw_all(self):
        for entity in self.entities:
            self.undraw_entity(entity)

    def update_and_draw_layout(self):
        for x, y in self:
            wall = self.is_wall(x, y)
            if self.visible(x, y):
                if wall:
                    self.update_and_draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('light_wall'))
                else:
                    self.update_and_draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('light_ground'))
                self.explored[x, y] = True
            elif self.explored[x, y]:
                if wall:
                    self.update_and_draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('dark_wall'))
                else:
                    self.update_and_draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('dark_ground'))

    def make_transparent_and_walkable(self, x, y):
        self.walkable[x, y] = True
        self.transparent[x, y] = True

    def within_bounds(self, x, y, buffer=0):
        return (
            (0 + buffer <= x < self.width - buffer) and
            (0 + buffer <= y < self.height - buffer))

    def visible(self, x, y):
        return self.fov[x, y] or self.illuminated[x, y]

    def is_wall(self, x, y):
            return (not self.shrub[x, y]
                    and not self.door[x, y]
                    and not self.transparent[x, y])

    def find_random_open_position(self):
        while True:
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            if self.walkable[x, y] and not self.blocked[x, y]:
                return x, y


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
