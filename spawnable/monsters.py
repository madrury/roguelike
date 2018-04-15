from enum import Enum, auto

from entity import Entity, EntityTypes
from render_functions import RenderOrder

from spawnable.spawnable import Spawnable
from etc.colors import COLORS
from components.ai import BasicMonster, HuntingMonster, SkitteringMonster
from components.attacker import Attacker
from components.harmable import Harmable



class Kruthik(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'k', COLORS['desaturated_green'], 'Kruthik', 
            entity_type=EntityTypes.MONSTER,
            attacker=Attacker(power=1),
            harmable=Harmable(hp=1, defense=0),
            ai=SkitteringMonster(),
            blocks=True,
            render_order=RenderOrder.ACTOR)


class Orc(Spawnable):
    
    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'O', COLORS['desaturated_green'], 'Orc', 
            entity_type=EntityTypes.MONSTER,
            attacker=Attacker(power=3),
            harmable=Harmable(hp=10, defense=0),
            ai=BasicMonster(),
            blocks=True,
            render_order=RenderOrder.ACTOR)


class Troll(Spawnable):
         
    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'T', COLORS['darker_green'], 'Troll', 
            entity_type=EntityTypes.MONSTER,
            attacker=Attacker(power=4),
            harmable=Harmable(hp=16, defense=1),
            ai=HuntingMonster(),
            blocks=True,
            render_order=RenderOrder.ACTOR)
            

MONSTER_GROUPS = {
    MonsterGroups.NONE: [],
    MonsterGroups.SINGLE_ORC: [Orc],
    MonsterGroups.THREE_ORCS: [Orc, Orc, Orc],
    MonsterGroups.SINGLE_TROLL: [Troll],
    MonsterGroups.TWO_ORCS_AND_TROLL: [Orc, Orc, Orc],
    MonsterGroups.KRUTHIK_SQARM: [Kruthik]*10
}


MONSTER_SCHEDULE = [
    (0.5, MonsterGroups.NONE),
    (0.5*0.2, MonsterGroups.SINGLE_ORC),
    (0.5*0.3, MonsterGroups.THREE_ORCS),
    (0.5*0.2, MonsterGroups.SINGLE_TROLL),
    (0.5*0.1, MonsterGroups.TWO_ORCS_AND_TROLL),
    (0.5*0.2, MonsterGroups.KRUTHIK_SQARM),
]
