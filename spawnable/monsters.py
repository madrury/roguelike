from entity import Entity

from spawnable.spawnable import Spawnable
from etc.colors import COLORS
from etc.enum import RenderOrder, EntityTypes, MonsterGroups, RoutingOptions
from components.ai import BasicMonster, HuntingMonster, SkitteringMonster
from components.attacker import Attacker
from components.harmable import Harmable
from components.burnable import AliveBurnable
from components.scaldable import AliveScaldable


class Kruthik(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'k', COLORS['desaturated_green'], 'Kruthik', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_WATER,
                           RoutingOptions.AVOID_FIRE,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_STEAM],
            attacker=Attacker(power=2),
            harmable=Harmable(hp=1, defense=0),
            ai=SkitteringMonster(),
            burnable=AliveBurnable(),
            scaldable=AliveScaldable())


class Orc(Spawnable):
    
    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'O', COLORS['desaturated_green'], 'Orc', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_WATER,
                           RoutingOptions.AVOID_FIRE,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_STEAM],
            attacker=Attacker(power=3),
            harmable=Harmable(hp=10, defense=0),
            ai=BasicMonster(),
            burnable=AliveBurnable(),
            scaldable=AliveScaldable())


class Troll(Spawnable):
         
    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'T', COLORS['darker_green'], 'Troll', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_WATER,
                           RoutingOptions.AVOID_FIRE,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_STEAM],
            attacker=Attacker(power=4),
            harmable=Harmable(hp=16, defense=1),
            ai=HuntingMonster(),
            burnable=AliveBurnable(),
            scaldable=AliveScaldable())
            

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
