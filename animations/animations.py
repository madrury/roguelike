import tdl
from time import sleep
import random

from etc.config import SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_CONFIG
from etc.colors import COLORS


def random_yellow():
    rg = int(random.uniform(220, 226))
    return (rg, rg, int(random.uniform(0, 256)))


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
        if self.current_frame >= 1:
            missile_prior_location = self.path[self.current_frame - 1]
            if self.game_map.fov[
                missile_prior_location[0], missile_prior_location[1]]:
                self.map_console.draw_char(
                    missile_prior_location[0], missile_prior_location[1], 
                    ' ', COLORS.get('light_ground'), bg=COLORS.get('light_ground'))
        if missile_location == self.target:
            return True
        color = random_yellow()
        if self.game_map.fov[missile_location[0], missile_location[1]]:
            self.map_console.draw_char(
                missile_location[0], missile_location[1], 
                '*', color, color)
        self.current_frame += 1
        return False
