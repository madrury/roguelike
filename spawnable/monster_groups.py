from etc.enum import MonsterGroups
from entities.monsters import Orc, Troll, Kruthik


MONSTER_GROUPS = {
    MonsterGroups.NONE: [],
    MonsterGroups.SINGLE_ORC: [Orc],
    MonsterGroups.THREE_ORCS: [Orc, Orc, Orc],
    MonsterGroups.SINGLE_TROLL: [Troll],
    MonsterGroups.TWO_ORCS_AND_TROLL: [Orc, Orc, Troll],
    MonsterGroups.KRUTHIK_SQARM: [Kruthik]*10
}


MONSTER_SCHEDULE = [
    (0.5, MonsterGroups.NONE),
    (0.5*0.6, MonsterGroups.SINGLE_ORC),
    (0.5*0.1, MonsterGroups.THREE_ORCS),
    (0.5*0.1, MonsterGroups.SINGLE_TROLL),
    (0.5*0.1, MonsterGroups.TWO_ORCS_AND_TROLL),
    (0.5*0.1, MonsterGroups.KRUTHIK_SQARM),
]
