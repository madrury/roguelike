import random

from colors import random_red_or_yellow, random_grey
from entity import Entity
from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder
from etc.game_config import STEAM_DISSAPATE_PROBABILTY, STEAM_SPREAD_PROBABILTY

from components.commitable import BaseCommitable, FireCommitable, SteamCommitable
from components.dissipatable import FireDissipatable, SteamDissipatable
from components.shimmer import FireShimmer, SteamShimmer
from components.spreadable import FireSpreadable, SteamSpreadable


class Fire:
    """A fire entity.

    Fire entities can spread to neighbouring squares containing burnable
    material, or harm burnable anjacent entities.  It will also dissipate at a
    fixed probability every turn.
    """
    @staticmethod
    def make(game_map, x, y):
        fg_color = random_red_or_yellow()
        bg_color = random_red_or_yellow()
        return Entity(
            x, y, '^',
            name="Fire",
            fg_color=fg_color,
            bg_color=bg_color,
            entity_type=EntityTypes.FIRE,
            render_order=RenderOrder.TERRAIN,
            commitable=FireCommitable(),
            dissipatable=FireDissipatable(),
            shimmer=FireShimmer(),
            spreadable=FireSpreadable())

    def maybe_make(game_map, x, y, p):
        spawn = random.uniform(0, 1) < p 
        if spawn:
            return Fire.make(game_map, x, y)
        else:
            return None


class Steam:
    """A stteam entity.

    Steam entities can spread to all neighbouring squares, and harm entities in
    the same equare.  It will also dissipate at a probablity each turn that
    increases with each spread.
    """
    @staticmethod
    def make(game_map, x, y, 
             p_spread=STEAM_SPREAD_PROBABILTY, 
             p_dissipate=STEAM_DISSAPATE_PROBABILTY):
        fg_color = random_grey()
        bg_color = random_grey()
        return Entity(
            x, y, '~',
            name="Steam",
            fg_color=fg_color,
            bg_color=bg_color,
            entity_type=EntityTypes.STEAM,
            render_order=RenderOrder.TERRAIN,
            commitable=SteamCommitable(),
            dissipatable=SteamDissipatable(p=p_dissipate),
            shimmer=SteamShimmer(),
            spreadable=SteamSpreadable(p=p_spread))


