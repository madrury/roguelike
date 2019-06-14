from entity import Entity

from etc.colors import COLORS
from etc.enum import (
    RenderOrder, EntityTypes, RoutingOptions, Elements)

from components.attacker import Attacker
from components.burnable import AliveBurnable, ZombieBurnable, WaterBloatBurnable
from components.commitable import BlockingCommitable
from components.defender import Defender
from components.freezable import EnemyFreezable
from components.movable import Movable
from components.scaldable import AliveScaldable, FireBloatScaldable
from components.spreadable import ZombieSpreadable
from components.swimmable import BaseSwimmable
import components.harmable
import components.ai

from components.transformers.damage_transformers import DefensiveLinearTransformer


class Kruthik:

    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'k', COLORS['kruthik'], 'Kruthik', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_WATER,
                           RoutingOptions.AVOID_FIRE,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_DOORS,
                           RoutingOptions.AVOID_STAIRS,
                           RoutingOptions.AVOID_STEAM],
            ai=components.ai.SkitteringMonster(),
            attacker=Attacker(power=2),
            burnable=AliveBurnable(),
            commitable=BlockingCommitable(),
            harmable=components.harmable.Harmable(hp=1, defense=0),
            freezable=EnemyFreezable(),
            movable=Movable(),
            scaldable=AliveScaldable(),
            swimmable=BaseSwimmable())


class Orc:
    
    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'O', COLORS['orc'], 'Orc', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_WATER,
                           RoutingOptions.AVOID_FIRE,
                           RoutingOptions.AVOID_SHRUBS,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_DOORS,
                           RoutingOptions.AVOID_STAIRS,
                           RoutingOptions.AVOID_STEAM],
            ai=components.ai.BasicMonster(),
            attacker=Attacker(power=3),
            burnable=AliveBurnable(),
            commitable=BlockingCommitable(),
            harmable=components.harmable.Harmable(hp=10, defense=0),
            freezable=EnemyFreezable(),
            movable=Movable(),
            swimmable=BaseSwimmable(),
            scaldable=AliveScaldable())


class PinkJelly:

    @staticmethod
    def make(x, y, *, hp=20):
        return Entity(
            x, y, 'J', COLORS['pink_jelly'], 'Pink Jelly', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_WATER,
                           RoutingOptions.AVOID_FIRE,
                           RoutingOptions.AVOID_SHRUBS,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_STAIRS,
                           RoutingOptions.AVOID_STEAM],
            ai=components.ai.BasicMonster(),
            attacker=Attacker(power=3),
            burnable=AliveBurnable(),
            commitable=BlockingCommitable(),
            harmable=components.harmable.PinkJellyHarmable(
                hp=hp, defense=0),
            freezable=EnemyFreezable(),
            movable=Movable(),
            swimmable=BaseSwimmable(),
            scaldable=AliveScaldable())

    def make_if_possible(game_map, x, y, hp=20):
        if (game_map.within_bounds(x, y) 
            and game_map.walkable[x, y]
            and not game_map.water[x, y]):
            return PinkJelly.make(x, y, hp=hp)


class Troll:
         
    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'T', COLORS['troll'], 'Troll', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_WATER,
                           RoutingOptions.AVOID_FIRE,
                           RoutingOptions.AVOID_SHRUBS,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_STAIRS,
                           RoutingOptions.AVOID_STEAM],
            attacker=Attacker(power=6),
            harmable=components.harmable.Harmable(hp=20, defense=1),
            ai=components.ai.HuntingMonster(),
            burnable=AliveBurnable(),
            commitable=BlockingCommitable(),
            freezable=EnemyFreezable(),
            movable=Movable(),
            swimmable=BaseSwimmable(),
            scaldable=AliveScaldable())


class FireBloat:

    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'b', COLORS['fire_bloat'], 'Fire Bloat', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_SHRUBS,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_DOORS,
                           RoutingOptions.AVOID_STAIRS,
                           RoutingOptions.AVOID_STEAM],
            ai=components.ai.BasicMonster(),
            attacker=Attacker(power=1),
            commitable=BlockingCommitable(),
            harmable=components.harmable.FireBloatHarmable(hp=1, defense=0),
            freezable=EnemyFreezable(),
            movable=Movable(),
            scaldable=FireBloatScaldable())


class WaterBloat:

    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'b', COLORS['water_bloat'], 'Water Bloat', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_SHRUBS,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_DOORS,
                           RoutingOptions.AVOID_STAIRS,
                           RoutingOptions.AVOID_FIRE],
            ai=components.ai.BasicMonster(),
            attacker=Attacker(power=1),
            burnable=WaterBloatBurnable(),
            commitable=BlockingCommitable(),
            harmable=components.harmable.WaterBloatHarmable(hp=1, defense=0),
            freezable=EnemyFreezable(),
            movable=Movable())


class Zombie:

    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'Z', COLORS['zombie'], 'Zombie', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_WATER,
                           RoutingOptions.AVOID_FIRE,
                           RoutingOptions.AVOID_SHRUBS,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_DOORS,
                           RoutingOptions.AVOID_STAIRS,
                           RoutingOptions.AVOID_STEAM],
            attacker=Attacker(power=3),
            defender=Defender(
                damage_transformers=[
                    DefensiveLinearTransformer(
                        elements=[Elements.NONE]),
                    DefensiveLinearTransformer(
                        elements=[Elements.FIRE], multiplyer=2),
                    DefensiveLinearTransformer(
                        elements=[Elements.HEALING], multiplyer=-1)]),
            harmable=components.harmable.Harmable(
                hp=10, defense=0),
            ai=components.ai.ZombieMonster(),
            burnable=ZombieBurnable(),
            commitable=BlockingCommitable(),
            freezable=EnemyFreezable(),
            movable=Movable(),
            scaldable=AliveScaldable(),
            swimmable=BaseSwimmable(),
            spreadable=ZombieSpreadable())


class Necromancer:
    
    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'N', COLORS['necromancer'], 'Necromancer', 
            entity_type=EntityTypes.MONSTER,
            blocks=True,
            render_order=RenderOrder.ACTOR,
            routing_avoid=[RoutingOptions.AVOID_WATER,
                           RoutingOptions.AVOID_FIRE,
                           RoutingOptions.AVOID_SHRUBS,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_STAIRS,
                           RoutingOptions.AVOID_STEAM],
            ai=components.ai.NecromancerMonster(),
            attacker=Attacker(power=5),
            burnable=AliveBurnable(),
            commitable=BlockingCommitable(),
            defender=Defender(
                damage_transformers=[
                    DefensiveLinearTransformer(
                        elements=[Elements.NONE]),
                    DefensiveLinearTransformer(
                        elements=[Elements.FIRE], multiplyer=2),
                    DefensiveLinearTransformer(
                        elements=[Elements.HEALING], multiplyer=-1)]),
            harmable=components.harmable.Harmable(
                hp=20, defense=0),
            freezable=EnemyFreezable(),
            movable=Movable(),
            swimmable=BaseSwimmable(),
            scaldable=AliveScaldable())
