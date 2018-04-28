from tdl.map import Map
import numpy as np
from random import randint, choice

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

    def draw_char(self, x, y, char, fg=None, bg=None):
        self.fg_colors[x, y] = fg
        self.bg_colors[x, y] = bg
        self.chars[x, y] = char
        self.console.draw_char(x, y, char, fg, bg)

    def render_all(self, entities, fov_recompute):
        # Draw walls.
        if fov_recompute:
            self._draw_walls() 
        # Draw Entities.
        entities_in_render_order = sorted(
            entities, key=lambda x: x.render_order.value)
        for entity in entities_in_render_order:
            self._draw_entity(entity)

    def clear_all(self, entities):
        for entity in entities:
            self._clear_entity(entity)

    def _draw_walls(self):
        for x, y in self:
            wall = not self.transparent[x, y]
            if self.fov[x, y]:
                if wall:
                    self.draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('light_wall'))
                else:
                    self.draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('light_ground'))
                self.explored[x, y] = True
            elif self.explored[x, y]:
                if wall:
                    self.draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('dark_wall'))
                else:
                    self.draw_char(
                        x, y, ' ', fg=None, bg=COLORS.get('dark_ground'))

    def _draw_entity(self, entity):
        bg_color = self.bg_colors[entity.x, entity.y]
        if self.fov[entity.x, entity.y]:
            self.draw_char(
                entity.x, entity.y, entity.char, 
                fg=entity.color, bg=bg_color)

    def _clear_entity(self, entity):
        bg_color = self.bg_colors[entity.x, entity.y]
        self.draw_char(
            entity.x, entity.y, ' ', entity.color, bg=bg_color)


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
