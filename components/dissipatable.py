import random
from etc.enum import ResultTypes
from etc.config import PROBABILITIES


class FireDissipatable:
    """Fire dissipates at a fixed probabilitiy every turn."""
    def __init__(self, p=PROBABILITIES['fire_dissipate']):
        self.p = p

    def dissipate(self, game_map):
        if random.uniform(0, 1) < self.p:
            return [{ResultTypes.REMOVE_ENTITY: self.owner}]
        else:
            return []


class SteamDissipatable:
    """Steam lingers for a number of frames, and then dissipates at a fixed
    probability during all subsequent turns.
    """
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
            return [{ResultTypes.REMOVE_ENTITY: self.owner}]
        else:
            return []


class NecroticSoilDissipatable:

    def __init__(self, n_frames=3):
        self.n_frames = n_frames
        self.frame = 0

    def dissipate(self, game_map):
        if self.frame < self.n_frames:
            self.frame += 1
            return []
        else:
            return [{ResultTypes.REMOVE_ENTITY: self.owner}]
