COLORS = {
    'dark_wall': (30, 30, 30),
    'dark_ground': (60, 60, 60),
    'light_wall': (110, 110, 110),
    'light_ground': (200, 200, 200),
    'light_grass': (0, 150, 0),
    'dark_grass': (0, 80, 0),
    'necrotic_soil': (90, 60, 30),

    'orc': (46, 139, 87),
    'troll': (128, 128, 0),
    'kruthik': (160, 82, 45),
    'pink_jelly': (255, 20, 147),
    'fire_bloat': (240, 0, 0),
    'water_bloat': (140, 140, 255),
    'zombie': (145, 145, 0),
    'necromancer': (50, 50, 50),

    'cursor': (255, 215, 0),
    'cursor_tail': (220, 180, 0), 

    'black': (0, 0, 0),
    'blue': (0, 0, 255),
    'dark_blue': (60, 60, 150),
    'dark_red': (191, 0, 0),
    'darker_green': (0, 127, 0),
    'darker_red': (127, 0, 0),
    'desaturated_green': (63, 127, 63),
    'green': (0, 255, 0),
    'light_blue': (150, 150, 230),
    'light_red': (255, 144, 144),
    'light_purple': (100, 0, 100),
    'dark_purple': (200, 0, 200),
    'medium_grey': (125, 125, 125),
    'orange': (255, 127, 0),
    'red': (255, 0, 0),
    'violet': (127, 0, 255),    
    'white': (255, 255, 255),
    'yellow': (255, 255, 0),
    'dark_yellow': (200, 200, 0),
    'very_dark_yellow': (150, 150, 0),
    'brown': (139, 69, 19),
    'dark_brown': (109, 49, 10)
}

STATUS_BAR_COLORS = {
    'hp_bar': {
        'bar_color': COLORS['light_red'],
        'back_color': COLORS['darker_red'],
        'string_color': COLORS['white']
    },
    'swim_bar': {
        'bar_color': COLORS['light_blue'],
        'back_color': COLORS['dark_blue'],
        'string_color': COLORS['white']
    },
    'confused_bar': {
        'bar_color': COLORS['dark_purple'],
        'back_color': COLORS['light_purple'],
        'string_color': COLORS['white']
    },
    'speedy_bar': {
        'bar_color': COLORS['dark_yellow'],
        'back_color': COLORS['very_dark_yellow'],
        'string_color': COLORS['white']
    }
}
