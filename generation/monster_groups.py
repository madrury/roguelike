from enum import Enum, auto

from game_objects.monsters import (
    Orc, Troll, Kruthik, PinkJelly, FireBloat, WaterBloat,
    Zombie, Necromancer)
from generation.scheduler import CompositeScheduler


class MonsterSpawnGroups(Enum):
    NONE = auto()
    SINGLE_ORC = auto()
    THREE_ORCS = auto()
    SINGLE_TROLL = auto()
    TWO_ORCS_AND_TROLL = auto()
    KRUTHIKS = auto()
    PINK_JELLY = auto()
    FIRE_BLOAT = auto()
    WATER_BLOAT = auto()
    ZOMBIE = auto()
    NECROMANCER = auto()

MONSTER_SPAWN_GROUPS = {
    MonsterSpawnGroups.NONE: [],
    MonsterSpawnGroups.SINGLE_ORC: [Orc],
    MonsterSpawnGroups.THREE_ORCS: [Orc, Orc, Orc],
    MonsterSpawnGroups.SINGLE_TROLL: [Troll],
    MonsterSpawnGroups.TWO_ORCS_AND_TROLL: [Orc, Orc, Troll],
    MonsterSpawnGroups.KRUTHIKS: [Kruthik]*10,
    MonsterSpawnGroups.PINK_JELLY: [PinkJelly],
    MonsterSpawnGroups.FIRE_BLOAT: [FireBloat],
    MonsterSpawnGroups.WATER_BLOAT: [WaterBloat],
    MonsterSpawnGroups.ZOMBIE: [Zombie],
    MonsterSpawnGroups.NECROMANCER: [Necromancer]
}


class MonsterSchedule(CompositeScheduler):
    default_group = MonsterSpawnGroups.NONE


class MonsterSpawnSchedules(Enum):
    NONE = auto()
    # Atomic monster spawn schedules.  Others are from combining these
    #  by weighting probabilities.
    ORCS = auto()
    TROLLS = auto()
    KRUTHIKS = auto()
    UNDEAD = auto()
    BLOATS = auto()
    # Non-atomic spawn schedules.
    ORCS_AND_KRUTHIKS = auto()
    ORCS_AND_TROLLS = auto()
    ORCS_AND_BLOATS = auto()
    TROLLS_AND_BLOATS = auto()

# Here we just define the atomic groups.
MONSTER_SPAWN_SCHEDULES = {
    MonsterSpawnSchedules.NONE: MonsterSchedule(),
    MonsterSpawnSchedules.ORCS: MonsterSchedule({
            MonsterSpawnGroups.NONE: 0.4,
            MonsterSpawnGroups.SINGLE_ORC: 0.4,
            MonsterSpawnGroups.THREE_ORCS: 0.2
    }),
    MonsterSpawnSchedules.KRUTHIKS: MonsterSchedule({
        MonsterSpawnGroups.NONE: 0.7,
        MonsterSpawnGroups.KRUTHIKS: 0.3
    }),
    MonsterSpawnSchedules.TROLLS: MonsterSchedule({
        MonsterSpawnGroups.NONE: 0.5,
        MonsterSpawnGroups.SINGLE_TROLL: 0.4,
        MonsterSpawnGroups.TWO_ORCS_AND_TROLL: 0.2
    }),
    MonsterSpawnSchedules.BLOATS: MonsterSchedule({
        MonsterSpawnGroups.NONE: 0.4,
        MonsterSpawnGroups.FIRE_BLOAT: 0.3,
        MonsterSpawnGroups.WATER_BLOAT: 0.3
    }),
    MonsterSpawnSchedules.UNDEAD: MonsterSchedule({
        MonsterSpawnGroups.NONE: 0.4,
        MonsterSpawnGroups.ZOMBIE: 0.4,
        MonsterSpawnGroups.NECROMANCER: 0.2
    })
}

# Non-atomic groups are composed by combining the atomic groups.
MONSTER_SPAWN_SCHEDULES.update({
    MonsterSpawnSchedules.ORCS_AND_KRUTHIKS: (
        MONSTER_SPAWN_SCHEDULES[MonsterSpawnSchedules.ORCS] |
        MONSTER_SPAWN_SCHEDULES[MonsterSpawnSchedules.KRUTHIKS]
    ),
    MonsterSpawnSchedules.ORCS_AND_BLOATS: (
        MONSTER_SPAWN_SCHEDULES[MonsterSpawnSchedules.ORCS] |
        MONSTER_SPAWN_SCHEDULES[MonsterSpawnSchedules.BLOATS]
    ),
    MonsterSpawnSchedules.ORCS_AND_TROLLS: (
        MONSTER_SPAWN_SCHEDULES[MonsterSpawnSchedules.ORCS] |
        MONSTER_SPAWN_SCHEDULES[MonsterSpawnSchedules.TROLLS]
    ),
    MonsterSpawnSchedules.TROLLS_AND_BLOATS: (
        MONSTER_SPAWN_SCHEDULES[MonsterSpawnSchedules.TROLLS] |
        MONSTER_SPAWN_SCHEDULES[MonsterSpawnSchedules.BLOATS]
    ),
})