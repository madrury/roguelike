ANIMATION_INTERVAL = 0.075
INVENTORY_WIDTH = 50
SCREEN_HEIGHT = 50
SCREEN_WIDTH = 80
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

TERRAIN_CONFIG = {
    'min_pools': 2,
    'max_pools': 5,
    'pool_room_proportion': 0.7,
    'min_ice': 2,
    'max_ice': 5,
    'ice_room_proportion': 0.7,
    'min_rivers': 1,
    'max_rivers': 3,
    'min_grass': 1,
    'max_grass': 3,
    'grass_room_proportion': 2.0,
    'min_shrubs': 1,
    'max_shrubs': 3,
    'shrubs_room_proportion': 2.0
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
