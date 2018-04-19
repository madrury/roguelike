SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50

FLOOR_CONFIG = {
    'width': 80,
    'height': 43,
    'max_rooms': 50,
}

ROOM_CONFIG = {
    'width': 10,
    'height': 10,
    'max_rectangles': 5,
    'max_rectangle_width': 3,
    'max_rectangle_height': 3,
}

MAP_CONFIG = {
    'max_monsters_per_room': 3,
    'max_items_per_room': 2
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
