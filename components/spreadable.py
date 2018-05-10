import random

from entity import get_entities_at_location
from etc.config import PROBABILITIES
from etc.enum import ResultTypes
from utils.utils import random_adjacent
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

    def spread(self, game_map, entities, p=PROBABILITIES["steam_spread"]):
        results = []
        new_x, new_y = random_adjacent((self.owner.x, self.owner.y))
        if random.uniform(0, 1) < p and game_map.within_bounds(new_x, new_y):
            steam = spawnable.various.Steam.make(game_map, new_x, new_y)
            if steam:
                results.append({ResultTypes.ADD_ENTITY: steam})
        return results
