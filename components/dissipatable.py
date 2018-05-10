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


class SteamDissipatable:

    def __init__(self, p=PROBABILITIES['steam_dissipate'],
                       n_frames=3):
        self.p_dissipate = p
        self.n_frames = n_frames
        self.frame = 0

    def dissipate(self, game_map):
        if self.frame < self.n_frames:
            self.frame += 1
            return []
        elif random.uniform(0, 1) < self.p_dissipate:
            game_map.steam[self.owner.x, self.owner.y] = False
            return [{ResultTypes.REMOVE_ENTITY: self.owner}]
        else:
            return []
