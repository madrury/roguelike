import numpy as np
from itertools import product
from random import randint, choice

from tdl.map import Map

from etc.colors import COLORS


class GameMap(Map):

    def __init__(self, width, height, console):
        super().__init__(width, height)
        self.console = console
        self.explored = np.zeros((width, height)).astype(bool)
        self.fg_colors = ColorArray((width, height))
        self.bg_colors = ColorArray((width, height))
        self.chars = np.full((width, height), ' ')

    def within_bounds(self, x, y):
        return (0 <= x < self.width) and (0 <= y < self.height)

    def make_transparent_and_walkable(self, x, y):
        self.walkable[x, y] = True
        self.transparent[x, y] = True

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

    # TODO: Is this needed?
    def draw_position(self, x, y):
        char = self.chars[x, y]
        fg = self.fg_colors[x, y]
        bg = self.bg_colors[x, y]
        self.draw_char(x, y, char, fg=fg, bg=bg)

    # TODO: Is this needed?
    def draw_all(self):
        it = zip(product(range(self.width), range(self.height)),
                 self.chars.flatten(),
                 self.fg_colors.flatten(),
                 self.bg_colors.flatten())
        for (x, y), char, fg_color, bg_color in it:
            self.draw_char(x, y, char, fg, bg)

    def update_and_draw_char(self, x, y, char, fg=None, bg=None):
        self.update_position(x, y, char, fg, bg)
        self.console.draw_char(x, y, char, fg, bg)

    def update_and_draw_all(self, entities, fov_recompute=True):
        # Draw walls.
        if fov_recompute:
            self.update_and_draw_layout() 
        # Draw Entities.
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
            if self.fov[x, y]:
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


class ColorArray:

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
