import random

from etc.game_config import FIRE_SPREAD_PROBABILITY, STEAM_SPREAD_PROBABILTY
from etc.enum import ResultTypes, EntityTypes
from utils.utils import (
    adjacent_coordinates, random_adjacent, get_all_entities_of_type_in_position)
import game_objects.terrain


class FireSpreadable:
    """Fire spreads to a random adjacent space containing a burnable entity at
    a fixed probability.
    """
    def __init__(self, p=FIRE_SPREAD_PROBABILITY):
        self.p_spread = p

    def spread(self, game_map):
        new_x, new_y = random_adjacent((self.owner.x, self.owner.y))
        entities_at_location = game_map.entities.get_entities_at_position(
            game_map, new_x, new_y)
        burnable_entities = [entity for entity in entities_at_location
                             if entity.burnable]
        results = []
        for entity in burnable_entities:
            if random.uniform(0, 1) < self.p_spread:
                results.extend(entity.burnable.burn(game_map))
        return results


class SteamSpreadable:
    """Steam spreads to all adjacent coordinates, each with a fixed probability.

    New steam that are the result of spreading are more likely to dissipate
    quickly, and less likely to spread.
    """
    def __init__(self, p=STEAM_SPREAD_PROBABILTY):
        self.p_spread = p

    def spread(self, game_map):
        results = []
        adjacent = adjacent_coordinates((self.owner.x, self.owner.y))
        for new_x, new_y in adjacent:
            if (random.uniform(0, 1) < self.p_spread and 
                game_map.within_bounds(new_x, new_y) and
                game_map.walkable[new_x, new_y]):
                new_p_spread = max(0, self.p_spread - 0.4)
                new_p_dissipate = min(1, self.owner.dissipatable.p_dissipate + 0.4)
                steam = game_objects.various.Steam.make(
                    game_map, new_x, new_y,
                    p_spread=new_p_spread,
                    p_dissipate=new_p_dissipate)
                if steam:
                    results.append({ResultTypes.ADD_ENTITY: steam})
        return results


class ZombieSpreadable:
     """Zombies spread necrotic soil to wherever they are standing."""
     def spread(self, game_map):
         results = []
         current_terrain = get_all_entities_of_type_in_position(
            (self.owner.x, self.owner.y), game_map, EntityTypes.TERRAIN) 
         for terrain in current_terrain:
             # If the zombie is drowning, it should not be able to remove water
             # by spawning necrotic soul.
             if not game_map.water[self.owner.x, self.owner.y]:
                results.append({ResultTypes.REMOVE_ENTITY: terrain})
         necrotic_soil = game_objects.terrain.NecroticSoil.make(
             game_map, self.owner.x, self.owner.y)
         results.append({ResultTypes.ADD_ENTITY: necrotic_soil})
         return results
