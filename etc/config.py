ANIMATION_INTERVAL = 0.075
INVENTORY_WIDTH = 50
SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50
SHIMMER_INTERVAL = 50

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
    'max_rivers': 3,
    'min_grass': 1,
    'max_grass': 3,
    'grass_room_proportion': 2.0
}

PANEL_CONFIG = {
    'bar_width': 20,
    'height': 7,
}
PANEL_CONFIG['y'] = SCREEN_HEIGHT - PANEL_CONFIG['height']

MESSAGE_CONFIG = {
    'x': 2*PANEL_CONFIG['bar_width'] + 3,
    'width': SCREEN_WIDTH - 2*PANEL_CONFIG['bar_width'] - 3,
    'height': PANEL_CONFIG['height'] - 1
}

FOV_CONFIG = {
    "algorithm": 'DIAMOND',
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

PROBABILITIES = {
    'grass_burn': 1.0,
    'fire_spread': 0.9,
    'steam_spread': 0.8,
    'fire_dissipate': 0.2,
    'steam_dissipate': 0.5
}
