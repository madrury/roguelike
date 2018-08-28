from enum import Enum, auto


class FloorType(Enum):
    STANDARD = auto()
    FIRST = auto()


FIRST_FLOOR = {
    'type': FloorType.FIRST,
    'width': 15,
    'height': 15,
    'max_rectangles': 3,
    'max_rectangle_width': 8,
    'max_rectangle_height': 8,
    'max_rooms': 20,
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
