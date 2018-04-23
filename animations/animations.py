import tdl
from time import sleep
import random

from utils.utils import coordinates_within_circle
from etc.config import SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_CONFIG
from etc.colors import COLORS
from etc.chars import CHARS
from animations.colors import COLOR_PATHS, random_yellow, random_red_or_yellow


class HealthPotionAnimation:

    # TODO: For consistency, target should be a position not an entity.
    def __init__(self, map_console, game_map, target):
        self.map_console = map_console
        self.game_map = game_map
        self.target = target
        self.color_iter = iter(COLOR_PATHS['dark_to_light_green'])

    def next_frame(self):
        try:
            self.map_console.draw_char(
                self.target.x, self.target.y, self.target.char, self.target.color,
                bg=COLORS['light_ground'])
            color = next(self.color_iter)
        except StopIteration:
            return True
        self.map_console.draw_char(
            self.target.x, self.target.y, self.target.char, self.target.color,
            bg=color)
        return False
        

class MagicMissileAnimation:

    def __init__(self, map_console, game_map, source, target):
        self.map_console = map_console
        self.source = source
        self.game_map = game_map
        self.target = target
        self.path = game_map.compute_path(
            source[0], source[1], target[0], target[1])
        self.char = '*'
        self.current_frame = 0

    def next_frame(self):
        return draw_missile(self, random_yellow(), random_yellow())


class FireblastAnimation:

    # TODO: For consistency, source should be a position not an entity.
    def __init__(self, map_console, game_map, source, radius=4):
        self.map_console = map_console
        self.game_map = game_map
        self.source = source
        self.radius = radius
        self.radius_iter = iter(range(radius + 1))

    def next_frame(self):
        try:
            blast_radius = next(self.radius_iter)
        # Clear the drawing of the blast, the animation has finished.
        except StopIteration:
            clear_coordinates = coordinates_within_circle(
                (self.source[0], self.source[1]), self.radius)
            for x, y in clear_coordinates:
                if (self.game_map.within_bounds(x, y) and 
                    self.game_map.fov[x, y] and 
                    self.game_map.walkable[x, y]):
                    self.map_console.draw_char(
                        x, y, ' ', 
                        COLORS.get('light_ground'), 
                        bg=COLORS.get('light_ground'))
            return True
        # Draw a red circle centered at `source`.
        blast_coordinates = coordinates_within_circle(
            (self.source[0], self.source[1]), blast_radius)
        for x, y in blast_coordinates:
            if (self.game_map.within_bounds(x, y) and 
                self.game_map.fov[x, y] and 
                self.game_map.walkable[x, y]):
                self.map_console.draw_char(
                    x, y, '^', random_red_or_yellow(), random_red_or_yellow())
        return False


class ThrowingKnifeAnimation:

    def __init__(self, map_console, game_map, source, target):
        self.map_console = map_console
        self.game_map = game_map
        self.source = source
        self.target = target
        self.path = game_map.compute_path(
            source[0], source[1], target[0], target[1])
        self.char = self._get_char()
        self.current_frame = 0

    def _get_char(self):
        dx, dy = (self.path[1][0] - self.path[0][0],
                  self.path[1][1] - self.path[0][1])
        if (dx, dy) in ((-1, 1), (0, 1), (1, 1)):
            return CHARS['down_arrow']
        elif (dx, dy) in ((-1, -1), (0, -1), (1, -1)):
            return CHARS['up_arrow']
        elif (dx, dy) == (1, 0):
            return CHARS['left_arrow']
        else:
            return CHARS['right_arrow']
        raise ValueError('Path does not move away from starting position.')

    def next_frame(self):
        return draw_missile(self, COLORS['white'], None)


def draw_missile(animation, fg_color, bg_color):
    missile_location = animation.path[animation.current_frame]
    # Clear the previous frame's missile.
    if animation.current_frame >= 1:
        missile_prior_location = animation.path[animation.current_frame - 1]
        if animation.game_map.fov[
            missile_prior_location[0], missile_prior_location[1]]:
            animation.map_console.draw_char(
                missile_prior_location[0], missile_prior_location[1], 
                ' ', COLORS.get('light_ground'), bg=COLORS.get('light_ground'))
    # If the missile has reached the target, the animation is done.
    if missile_location == animation.target:
        return True
    # Draw the missile.
    if animation.game_map.fov[missile_location[0], missile_location[1]]:
        animation.map_console.draw_char(
            missile_location[0], missile_location[1], 
            animation.char, fg_color, bg_color)
    animation.current_frame += 1
    return False
