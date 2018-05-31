import random
from etc.enum import ResultTypes
from etc.game_config import (
    FIRE_DISSAPATE_PROBABILTY, STEAM_DISSAPATE_PROBABILTY,
    STEAM_DISSAPATE_N_FRAMES, NECROTIC_SOIL_DISSIPATE_N_FRAMES)


class FireDissipatable:
    """Fire dissipates at a fixed probabilitiy every turn."""
    def __init__(self, p=FIRE_DISSAPATE_PROBABILTY):
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
    def __init__(self, p=STEAM_DISSAPATE_PROBABILTY,
                       n_frames=STEAM_DISSAPATE_N_FRAMES):
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
    """Necrotic soil lingers for a fixed number of game turns before
    dissipating.
    """
    def __init__(self, n_frames=NECROTIC_SOIL_DISSIPATE_N_FRAMES):
        self.n_frames = n_frames
        self.frame = 0

    def dissipate(self, game_map):
        if self.frame < self.n_frames:
            self.frame += 1
            return []
        else:
            return [{ResultTypes.REMOVE_ENTITY: self.owner}]
