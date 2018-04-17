import tdl
from time import sleep
import random

from utils.utils import coordinates_within_circle
from etc.config import SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_CONFIG
from etc.colors import COLORS
from animations.colors import COLOR_PATHS, random_yellow, random_red


class HealthPotionAnimation:

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
        self.current_frame = 0

    def next_frame(self):
        missile_location = self.path[self.current_frame]
        # Clear the previous frame's missile.
        if self.current_frame >= 1:
            missile_prior_location = self.path[self.current_frame - 1]
            if self.game_map.fov[
                missile_prior_location[0], missile_prior_location[1]]:
                self.map_console.draw_char(
                    missile_prior_location[0], missile_prior_location[1], 
                    ' ', COLORS.get('light_ground'), bg=COLORS.get('light_ground'))
        # If the missile has reached the target, the animation is done.
        if missile_location == self.target:
            return True
        # Draw the missile in a random yellow color.
        color = random_yellow()
        if self.game_map.fov[missile_location[0], missile_location[1]]:
            self.map_console.draw_char(
                missile_location[0], missile_location[1], 
                '*', color, color)
        self.current_frame += 1
        return False


class FireblastAnimation:

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
                (self.source.x, self.source.y), self.radius)
            for x, y in clear_coordinates:
                self.map_console.draw_char(x, y, ' ', 
                    COLORS.get('light_ground'), bg=COLORS.get('light_ground'))
            return True
        # Draw a red circle centered at `source`.
        blast_coordinates = coordinates_within_circle(
            (self.source.x, self.source.y), blast_radius)
        for x, y in blast_coordinates:
            self.map_console.draw_char(x, y, '^', random_red(), random_red())
        return False
           
        
