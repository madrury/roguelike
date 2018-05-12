from entity import Entity

from etc.colors import COLORS
from etc.enum import RenderOrder, EntityTypes, MonsterGroups, RoutingOptions
from components.ai import BasicMonster, HuntingMonster, SkitteringMonster
from components.attacker import Attacker
from components.harmable import Harmable
from components.burnable import AliveBurnable
from components.movable import Movable
from components.scaldable import AliveScaldable


class Kruthik:

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
            movable=Movable(),
            scaldable=AliveScaldable())


class Orc:
    
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
            movable=Movable(),
            scaldable=AliveScaldable())


class Troll:
         
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
            movable=Movable(),
            scaldable=AliveScaldable())
