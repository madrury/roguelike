import random

from entity import get_entities_at_location
from etc.config import PROBABILITIES
from utils.utils import random_adjacent


class FireSpreadable:

    def spread(self, game_map, entities, p=PROBABILITIES['fire_spread']):
        new_x, new_y = random_adjacent((self.owner.x, self.owner.y))
        entities_at_location = get_entities_at_location(entities, new_x, new_y)
        burnable_entities = [entity for entity in entities_at_location
                             if entity.burnable]
        results = []
        for entity in burnable_entities:
            if random.uniform(0, 1) < p:
                results.extend(entity.burnable.burn())
        return results
