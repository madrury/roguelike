SCREEN_HEIGHT = 60 
SCREEN_WIDTH = 100

INVENTORY_WIDTH = 50

ANIMATION_INTERVAL = 0.075
SHIMMER_INTERVAL = 50


TOP_PANEL_CONFIG = {
    'bar_width': 20,
    'height': 3
}

BOTTOM_PANEL_CONFIG = {
    'bar_width': 20,
    'height': 7,
}
BOTTOM_PANEL_CONFIG['y'] = SCREEN_HEIGHT - BOTTOM_PANEL_CONFIG['height']

MAP_PANEL_CONFIG = {
    'y': TOP_PANEL_CONFIG['height']
}

MESSAGE_CONFIG = {
    'x': BOTTOM_PANEL_CONFIG['bar_width'] + 2,
    'width': SCREEN_WIDTH - 2*BOTTOM_PANEL_CONFIG['bar_width'] - 3,
    'height': BOTTOM_PANEL_CONFIG['height'] - 1
}

GLOBAL_FLOOR_CONFIG = {
    'width': SCREEN_WIDTH,
    'height': (SCREEN_HEIGHT
               - TOP_PANEL_CONFIG['height']
               - BOTTOM_PANEL_CONFIG['height']),
}

INITIAL_PLAYER_POSITION = (
    GLOBAL_FLOOR_CONFIG['width'] // 2,
    GLOBAL_FLOOR_CONFIG['height'] - 4)

FOV_CONFIG = {
    "algorithm": 'RESTRICTIVE',
    "light_walls": True,
    "radius": 10
}

PLAYER_CONFIG = {
    "char": '@',
    "color": "white",
    "defense": 2,
    "hp": 250,
    "inventory_size": 26,
    "name": "Player",
    "power": 5,
    "swim_stamina": 5,
}
