import random

from entity import get_entities_at_location
from etc.config import PROBABILITIES
from etc.enum import ResultTypes
from utils.utils import adjacent_coordinates, random_adjacent
import spawnable.various


class FireSpreadable:

    def spread(self, game_map, entities, p=PROBABILITIES['fire_spread']):
        new_x, new_y = random_adjacent((self.owner.x, self.owner.y))
        entities_at_location = get_entities_at_location(entities, new_x, new_y)
        burnable_entities = [entity for entity in entities_at_location
                             if entity.burnable]
        results = []
        for entity in burnable_entities:
            if random.uniform(0, 1) < p:
                results.extend(entity.burnable.burn(game_map))
        return results


class SteamSpreadable:

    def __init__(self, p=PROBABILITIES["steam_spread"]):
        self.p_spread = p

    def spread(self, game_map, entities, p=PROBABILITIES["steam_spread"]):
        results = []
        adjacent = adjacent_coordinates((self.owner.x, self.owner.y))
        for new_x, new_y in adjacent:
            if (random.uniform(0, 1) < self.p_spread and 
                game_map.within_bounds(new_x, new_y)):
                new_p_spread = max(0, self.p_spread - 0.4)
                new_p_dissipate = min(1, self.owner.dissipatable.p_dissipate + 0.4)
                steam = spawnable.various.Steam.make(
                    game_map, new_x, new_y,
                    p_spread=new_p_spread,
                    p_dissipate=new_p_dissipate)
                if steam:
                    results.append({ResultTypes.ADD_ENTITY: steam})
        return results
