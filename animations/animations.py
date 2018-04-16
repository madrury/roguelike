import tdl
from etc.config import SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_CONFIG
from etc.colors import COLORS
from time import sleep


class MagicMissileAnimation:

    def __init__(self, map_console, game_map, source, target):
        self.map_console = map_console
        self.source = source
        self.target = target
        self.path = game_map.compute_path(
            source[0], source[1], target[0], target[1])
        self.current_frame = 0

    def next_frame(self):

        print("Playing animation frame ", self.current_frame)
        missile_location = self.path[self.current_frame]
        if self.current_frame >= 1:
            missile_prior_location = self.path[self.current_frame - 1]
            self.map_console.draw_char(
                missile_prior_location[0], missile_prior_location[1], 
                ' ', COLORS.get('light_ground'), bg=COLORS.get('light_ground'))
        if missile_location == self.target:
            return True
        self.map_console.draw_char(
            missile_location[0], missile_location[1], 
            '*', COLORS.get('yellow'), bg=None)

        self.current_frame += 1
        return False
