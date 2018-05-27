import random

from etc.config import PROBABILITIES
from etc.enum import ResultTypes, EntityTypes
from utils.utils import (
    adjacent_coordinates, random_adjacent, get_entities_at_location,
    get_all_entities_of_type_in_position)
import game_objects.various


class FireSpreadable:
    """Fire spreads to a random adjacent space containing a burnable entity at
    a fixed probability.
    """
    def __init__(self, p=PROBABILITIES['fire_spread']):
        self.p_spread = p

    def spread(self, game_map):
        new_x, new_y = random_adjacent((self.owner.x, self.owner.y))
        entities_at_location = get_entities_at_location(game_map, new_x, new_y)
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
    def __init__(self, p=PROBABILITIES["steam_spread"]):
        self.p_spread = p

    def spread(self, game_map, p=PROBABILITIES["steam_spread"]):
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
             results.append({ResultTypes.REMOVE_ENTITY: terrain})
         necrotic_soil = game_objects.various.NecroticSoil.make(
             game_map, self.owner.x, self.owner.y)
         results.append({ResultTypes.ADD_ENTITY: necrotic_soil})
         return results
