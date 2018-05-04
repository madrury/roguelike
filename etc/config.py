SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

FLOOR_CONFIG = {
    'width': 80,
    'height': 43,
    'max_rooms': 20,
}

ROOM_CONFIG = {
    'width': 15,
    'height': 15,
    'max_rectangles': 3,
    'max_rectangle_width': 8,
    'max_rectangle_height': 8,
}

TERRAIN_CONFIG = {
    'min_pools': 2,
    'max_pools': 5,
    'pool_room_proportion': 0.7,
    'min_rivers': 1,
    'max_rivers': 3
}

PANEL_CONFIG = {
    'bar_width': 20,
    'height': 7,
}
PANEL_CONFIG['y'] = SCREEN_HEIGHT - PANEL_CONFIG['height']

MESSAGE_CONFIG = {
    'x': PANEL_CONFIG['bar_width'] + 2,
    'width': SCREEN_WIDTH - PANEL_CONFIG['bar_width'] - 2,
    'height': PANEL_CONFIG['height'] - 1
}

FOV_CONFIG = {
    "algorithm": 'DIAMOND',
    "light_walls": True,
    "radius": 10
}

SHIMMER_INTERVAL = 50

PROBABILITIES = {
    'grass_burn': 0.8,
    'fire_spread': 1.0,
    'fire_dissipate': 0.25
}
