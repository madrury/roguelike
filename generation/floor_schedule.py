from enum import Enum, auto

from etc.config import GLOBAL_FLOOR_CONFIG
from game_objects.terrain import StationaryTorch


class FloorType(Enum):
    STANDARD = auto()
    FIRST = auto()


floor_width_midpoint = GLOBAL_FLOOR_CONFIG['width'] // 2
floor_height = GLOBAL_FLOOR_CONFIG['height']
FIRST_FLOOR = {
    'type': FloorType.FIRST,
    'width': 15,
    'height': 15,
    'max_rectangles': 3,
    'max_rectangle_width': 8,
    'max_rectangle_height': 8,
    'max_rooms': 20,
    'first_room_width': 17,
    'first_room_height': 25,
    # Four rows of pillars surround the player in the first room.
    'objects': [
        StationaryTorch.make(None, floor_width_midpoint - 5, y) 
            for y in range(floor_height - 6, floor_height - 9*3, -3)] + [
        StationaryTorch.make(None, floor_width_midpoint - 3, y) 
            for y in range(floor_height - 6, floor_height - 9*3, -3)] + [
        StationaryTorch.make(None, floor_width_midpoint + 3, y)
            for y in range(floor_height - 6, floor_height - 9*3, -3)] + [
        StationaryTorch.make(None, floor_width_midpoint + 5, y)
            for y in range(floor_height - 6, floor_height - 9*3, -3)]
}

BASIC_FLOOR = {
    'type': FloorType.STANDARD,
    'width': 15,
    'height': 15,
    'max_rectangles': 3,
    'max_rectangle_width': 8,
    'max_rectangle_height': 8,
    'max_rooms': 20,
}


FLOOR_SCHEDULES = [
    FIRST_FLOOR,
    BASIC_FLOOR,
    BASIC_FLOOR
]
