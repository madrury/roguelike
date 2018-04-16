import tdl
from etc.config import SCREEN_WIDTH, SCREEN_HEIGHT, PANEL_CONFIG
from etc.colors import COLORS
from time import sleep


class MagicMissileAnimation:

    def __init__(self, root_console, map_console, game_map, source, target):
        self.root_console = root_console
        self.map_console = map_console
        self.source = source
        self.target = target
        self.path = game_map.compute_path(
            source[0], source[1], target[0], target[1])
        self.current_frame = 0

    def next_frame(self):
        print("Playing animation frame ", self.current_frame)
        missile_location = self.path[self.current_frame]
        if missile_location == self.target:
            return True

        self.map_console.draw_char(
            missile_location[0], missile_location[1], 
            '*', COLORS.get('yellow'), bg=COLORS.get('yellow'))
        self.root_console.blit(
            self.map_console, 0, PANEL_CONFIG['y'], 
            SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        sleep(0.5)

        self.map_console.draw_char(
            missile_location[0], missile_location[1], 
            ' ', COLORS.get('light_ground'), bg=COLORS.get('light_ground'))
        self.root_console.blit(
            self.map_console, 0, PANEL_CONFIG['y'], 
            SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        self.current_frame += 1
        return False
