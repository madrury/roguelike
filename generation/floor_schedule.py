from enum import Enum, auto

from generation.special_rooms import RoomType
from generation.terrain_schedule import TerrainTypes


class FloorType(Enum):
    STANDARD = auto()


FIRST_FLOOR = {
    'type': FloorType.STANDARD,
    'terrain_type': TerrainTypes.FIRST_FLOOR,
    'rooms': [RoomType.FIRST_ROOM],
    'width': 15,
    'height': 15,
    'max_rectangles': 3,
    'max_rectangle_width': 8,
    'max_rectangle_height': 8,
    'max_rooms': 20,
}


BASIC_FLOOR = {
    'type': FloorType.STANDARD,
    'terrain_type': TerrainTypes.BASIC_FLOOR,
    'rooms': [],
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
