import random

from colors import random_red_or_yellow, random_grey
from entity import Entity
from etc.enum import EntityTypes, RenderOrder
from etc.config import PROBABILITIES
from components.shimmer import FireShimmer, SteamShimmer
from components.spreadable import FireSpreadable, SteamSpreadable
from components.dissipatable import FireDissipatable, SteamDissipatable


class Fire:

    @staticmethod
    def make(game_map, x, y):
        if not game_map.fire[x, y]:
            game_map.fire[x, y] = True
            fg_color = random_red_or_yellow()
            bg_color = random_red_or_yellow()
            return Entity(
                x, y, '^',
                name="Fire",
                fg_color=fg_color,
                bg_color=bg_color,
                entity_type=EntityTypes.FIRE,
                render_order=RenderOrder.TERRAIN,
                shimmer=FireShimmer(),
                spreadable=FireSpreadable(),
                dissipatable=FireDissipatable())

    def maybe_make(game_map, x, y, p):
        spawn = random.uniform(0, 1) < p 
        if spawn:
            return Fire.make(game_map, x, y)
        else:
            return None


class Steam:

    @staticmethod
    def make(game_map, x, y, 
             p_spread=PROBABILITIES['steam_spread'], 
             p_dissipate=PROBABILITIES['steam_dissipate']):
        if not game_map.steam[x, y]:
            game_map.steam[x, y] = True
            fg_color = random_grey()
            bg_color = random_grey()
            return Entity(
                x, y, '~',
                name="Steam",
                fg_color=fg_color,
                bg_color=bg_color,
                entity_type=EntityTypes.STEAM,
                render_order=RenderOrder.TERRAIN,
                shimmer=SteamShimmer(),
                spreadable=SteamSpreadable(p=p_spread),
                dissipatable=SteamDissipatable(p=p_dissipate))
