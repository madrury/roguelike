from etc.enum import MonsterGroups
from game_objects.monsters import (
    Orc, Troll, Kruthik, PinkJelly, FireBloat, WaterBloat,
    Zombie, Necromancer)


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


class MonsterGroup:

    def __init__(self, group_distribution=None):
        if group_distribution:
            self.group_distribution = group_distribution
        else:
            self.group_distribution = [(1.0, MonsterGroups.NONE)]
    
    def __or__(self, other):
        for group in MonsterGroups:
            # YOU ARE HERE
            # First, you should probably convert these tuple things to dicts
            # Then you need to combine the probability distributions.
            pass
        return self


MONSTER_SCHEDULES = [
    [
        (0.5,    MonsterGroups.NONE),
        (0.3*1.0, MonsterGroups.SINGLE_ORC),
        (0.1*1.0, MonsterGroups.THREE_ORCS),
        (0.1*1.0, MonsterGroups.SINGLE_TROLL),
        (0.1*0.0, MonsterGroups.TWO_ORCS_AND_TROLL),
        (0.1*0.0, MonsterGroups.KRUTHIK_SQARM),
        (0.1*0.0, MonsterGroups.PINK_JELLY),
        (0.1*0.0, MonsterGroups.FIRE_BLOAT),
        (0.1*0.0, MonsterGroups.WATER_BLOAT),
        (0.1*0.0, MonsterGroups.ZOMBIE),
        (0.1*0.0, MonsterGroups.NECROMANCER)],
    [
        (0.5,     MonsterGroups.NONE),
        (0.5*0.5, MonsterGroups.SINGLE_ORC),
        (0.5*0.3, MonsterGroups.THREE_ORCS),
        (0.5*0.1, MonsterGroups.SINGLE_TROLL),
        (0.5*0.0, MonsterGroups.TWO_ORCS_AND_TROLL),
        (0.5*0.1, MonsterGroups.KRUTHIK_SQARM),
        (0.5*0.0, MonsterGroups.PINK_JELLY),
        (0.5*0.0, MonsterGroups.FIRE_BLOAT),
        (0.5*0.0, MonsterGroups.WATER_BLOAT),
        (0.5*0.0, MonsterGroups.ZOMBIE),
        (0.5*0.0, MonsterGroups.NECROMANCER)],
    [
        (0.5,     MonsterGroups.NONE),
        (0.5*0.3, MonsterGroups.SINGLE_ORC),
        (0.5*0.0, MonsterGroups.THREE_ORCS),
        (0.5*0.1, MonsterGroups.SINGLE_TROLL),
        (0.5*0.0, MonsterGroups.TWO_ORCS_AND_TROLL),
        (0.5*0.1, MonsterGroups.KRUTHIK_SQARM),
        (0.5*0.1, MonsterGroups.PINK_JELLY),
        (0.5*0.1, MonsterGroups.FIRE_BLOAT),
        (0.5*0.1, MonsterGroups.WATER_BLOAT),
        (0.5*0.1, MonsterGroups.ZOMBIE),
        (0.5*0.1, MonsterGroups.NECROMANCER)],
]
