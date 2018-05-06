from entity import Entity

from spawnable.spawnable import Spawnable
from etc.colors import COLORS
from etc.enum import RenderOrder, EntityTypes, MonsterGroups
from components.ai import BasicMonster, HuntingMonster, SkitteringMonster
from components.attacker import Attacker
from components.harmable import Harmable
from components.burnable import AliveBurnable



class Kruthik(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'k', COLORS['desaturated_green'], 'Kruthik', 
            entity_type=EntityTypes.MONSTER,
            attacker=Attacker(power=1),
            harmable=Harmable(hp=1, defense=0),
            ai=SkitteringMonster(),
            burnable=AliveBurnable(),
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
            burnable=AliveBurnable(),
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
            burnable=AliveBurnable(),
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
    (0.3, MonsterGroups.NONE),
    (0.7*0.3, MonsterGroups.SINGLE_ORC),
    (0.7*0.2, MonsterGroups.THREE_ORCS),
    (0.7*0.2, MonsterGroups.SINGLE_TROLL),
    (0.7*0.2, MonsterGroups.TWO_ORCS_AND_TROLL),
    (0.7*0.1, MonsterGroups.KRUTHIK_SQARM),
]
