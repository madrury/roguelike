from enum import Enum, auto

from generation.special_rooms import RoomType
from generation.terrain_schedule import TerrainTypes
from generation.monster_groups import MonsterSchedules, MONSTER_SCHEDULES


class FloorType(Enum):
    STANDARD = auto()


FIRST_FLOOR = {
    'type': FloorType.STANDARD,
    'terrain_type': TerrainTypes.FIRST_FLOOR,
    'monster_schedule': MONSTER_SCHEDULES[MonsterSchedules.NONE].to_list_of_tuples(),
    'rooms': [RoomType.FIRST_ROOM],
    'width': 15,
    'height': 15,
    'max_rectangles': 3,
    'max_rectangle_width': 8,
    'max_rectangle_height': 8,
    'max_rooms': 20,
}

BASIC_FLOOR_TEMPLATE = {
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


def create_floor_from_template(template, terrain_type, monster_schedule):
    floor_template = template.copy()
    floor_template['terrain_type'] = terrain_type
    floor_template['monster_schedule'] = MONSTER_SCHEDULES[monster_schedule].to_list_of_tuples()
    return floor_template


FLOOR_SCHEDULES = [
    FIRST_FLOOR,
    create_floor_from_template(
        BASIC_FLOOR_TEMPLATE,
        TerrainTypes.BASIC_FLOOR,
        MonsterSchedules.ORCS_AND_KRUTHIKS),
    create_floor_from_template(
        BASIC_FLOOR_TEMPLATE,
        TerrainTypes.SHRUB_FLOOR,
        MonsterSchedules.ORCS_AND_KRUTHIKS),
    # create_basic_floor(TerrainTypes.WATER_FLOOR),
    # create_basic_floor(TerrainTypes.ICE_FLOOR)
]
