# TODO: Move this enum into this file.
from enum import Enum, auto

from game_objects.monsters import (
    Orc, Troll, Kruthik, PinkJelly, FireBloat, WaterBloat,
    Zombie, Necromancer)

class MonsterSchedule:
    """Represent a schedule for spawning monsters on a floor, and implement
    an algebra of monster schedules with allows for combining them.
    """
    def __init__(self, group_distribution=None):
        if group_distribution:
            self.group_distribution = group_distribution
        else:
            self.group_distribution = {MonsterGroups.NONE: 1.0}

    def __or__(self, other):
        all_groups = set(self.group_distribution.keys()) | set(other.group_distribution.keys())
        total_probability = sum(
            self.group_distribution[group] + other.group_distribution[group]
            for group in all_groups
        )
        merged_groups = {
            group: (self.group_distribution[group] + other.group_distribution[group]) / total_probability
            for group in all_groups
        }
        return MonsterSchedule(group_distribution=merged_groups)

    def to_list_of_tuples(self):
        lot = []
        for group, prob in self.group_distribution.items():
            lot.append((prob, group))
        return lot


class MonsterGroups(Enum):
    NONE = auto()
    SINGLE_ORC = auto()
    THREE_ORCS = auto()
    SINGLE_TROLL = auto()
    TWO_ORCS_AND_TROLL = auto()
    KRUTHIK_SQARM = auto()
    PINK_JELLY = auto()
    FIRE_BLOAT = auto()
    WATER_BLOAT = auto()
    ZOMBIE = auto()
    NECROMANCER = auto()

MONSTER_GROUPS = {
    MonsterGroups.NONE: [],
    MonsterGroups.SINGLE_ORC: [Orc],
    MonsterGroups.THREE_ORCS: [Orc, Orc, Orc],
    MonsterGroups.SINGLE_TROLL: [Troll],
    MonsterGroups.TWO_ORCS_AND_TROLL: [Orc, Orc, Troll],
    MonsterGroups.KRUTHIK_SQARM: [Kruthik]*10,
    MonsterGroups.PINK_JELLY: [PinkJelly],
    MonsterGroups.FIRE_BLOAT: [FireBloat],
    MonsterGroups.WATER_BLOAT: [WaterBloat],
    MonsterGroups.ZOMBIE: [Zombie],
    MonsterGroups.NECROMANCER: [Necromancer]
}


class MonsterSchedules(Enum):
    NONE = auto()
    ORCS_AND_KRUTHIKS = auto()
    TROLLS = auto()
    UNDEAD = auto()
    BLOATS = auto()

MONSTER_SCHEDULES = {
    MonsterSchedules.NONE: MonsterSchedule(),
    MonsterSchedules.ORCS_AND_KRUTHIKS: MonsterSchedule({
            MonsterGroups.NONE: 0.4,
            MonsterGroups.SINGLE_ORC: 0.3,
            MonsterGroups.THREE_ORCS: 0.1,
            MonsterGroups.KRUTHIK_SQARM: 0.2}),
    MonsterSchedules.TROLLS: MonsterSchedule({
        MonsterGroups.NONE: 0.5,
        MonsterGroups.SINGLE_TROLL: 0.4,
        MonsterGroups.TWO_ORCS_AND_TROLL: 0.2}),
    MonsterSchedules.BLOATS: MonsterSchedule({
        MonsterGroups.NONE: 0.4,
        MonsterGroups.FIRE_BLOAT: 0.3,
        MonsterGroups.WATER_BLOAT: 0.3}),
    MonsterSchedules.UNDEAD: MonsterSchedule({
        MonsterGroups.NONE: 0.4,
        MonsterGroups.ZOMBIE: 0.4,
        MonsterGroups.NECROMANCER: 0.2})
}