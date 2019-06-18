from enum import Enum, auto

from generation.special_rooms import RoomType
from generation.terrain_schedule import TerrainTypes
from generation.monster_groups import MonsterSpawnSchedules, MONSTER_SPAWN_SCHEDULES
from generation.item_groups import ItemSpawnSchedules, ITEM_SPAWN_SCHEDULES


def create_floor_from_template(template, terrain_type, monster_schedule, item_schedule):
    floor_template = template.copy()
    floor_template['terrain_type'] = terrain_type
    floor_template['monster_schedule'] = MONSTER_SPAWN_SCHEDULES[monster_schedule].to_list_of_tuples()
    floor_template['item_schedule'] = ITEM_SPAWN_SCHEDULES[item_schedule].to_list_of_tuples()
    return floor_template


class FloorType(Enum):
    ROOMS_AND_TUNNELS = auto()
    CAVE = auto()

FIRST_FLOOR = {
    'type': FloorType.ROOMS_AND_TUNNELS,
    'terrain_type': TerrainTypes.FIRST_FLOOR,
    'monster_schedule': MONSTER_SPAWN_SCHEDULES[MonsterSpawnSchedules.NONE].to_list_of_tuples(),
    'item_schedule': ITEM_SPAWN_SCHEDULES[ItemSpawnSchedules.NONE].to_list_of_tuples(),
    'rooms': [RoomType.FIRST_ROOM],
    'width': 15,
    'height': 15,
    'max_rectangles': 3,
    'max_rectangle_width': 8,
    'max_rectangle_height': 8,
    'max_rooms': 20,
}

ROOMS_AND_TUNNELS_TEMPLATE = {
    'type': FloorType.ROOMS_AND_TUNNELS,
    'terrain_type': TerrainTypes.BASIC_FLOOR,
    'rooms': [],
    'width': 15,
    'height': 15,
    'max_rectangles': 3,
    'max_rectangle_width': 8,
    'max_rectangle_height': 8,
    'max_rooms': 20,
}

CAVE_TEMPLATE = {
    'type': FloorType.CAVE,
    'terrain_type': TerrainTypes.BASIC_FLOOR,
    'rooms': []
}


FLOOR_SCHEDULES = [
    FIRST_FLOOR,
    create_floor_from_template(
        CAVE_TEMPLATE,
        TerrainTypes.BASIC_FLOOR,
        MonsterSpawnSchedules.ORCS_AND_KRUTHIKS,
        ItemSpawnSchedules.BASIC_POTIONS),
    create_floor_from_template(
        ROOMS_AND_TUNNELS_TEMPLATE,
        TerrainTypes.BASIC_FLOOR,
        MonsterSpawnSchedules.ORCS_AND_KRUTHIKS,
        ItemSpawnSchedules.BASIC_POTIONS),
    create_floor_from_template(
        ROOMS_AND_TUNNELS_TEMPLATE,
        TerrainTypes.SHRUB_FLOOR,
        MonsterSpawnSchedules.ORCS,
        ItemSpawnSchedules.BASIC_WEAPONS),
]
