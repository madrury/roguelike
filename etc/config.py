SCREEN_HEIGHT = 60 
SCREEN_WIDTH = 100

ANIMATION_INTERVAL = 0.075
INVENTORY_WIDTH = 50
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


FLOOR_CONFIG = {
    'width': 80,
    'height': (SCREEN_HEIGHT
               - TOP_PANEL_CONFIG['height']
               - BOTTOM_PANEL_CONFIG['height']),
    'max_rooms': 20,
}

ROOM_CONFIG = {
    'width': 15,
    'height': 15,
    'max_rectangles': 3,
    'max_rectangle_width': 8,
    'max_rectangle_height': 8,
}

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
