import random
from etc.enum import ResultTypes
from etc.config import PROBABILITIES

class FireDissipatable:

    def __init__(self, p=PROBABILITIES['fire_dissipate']):
        self.p = p

    def dissipate(self, game_map):
        if random.uniform(0, 1) < self.p:
            game_map.fire[self.owner.x, self.owner.y] = False
            return [{ResultTypes.REMOVE_ENTITY: self.owner}]
        else:
            return []