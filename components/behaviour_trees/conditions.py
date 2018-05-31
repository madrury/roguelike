import random

from utils.utils import l2_distance
from etc.enum import TreeStates


class IsAdjacent:
    """Return sucess is owner is adjacent to target."""
    def tick(self, owner, target, game_map, context):
        distance = l2_distance((owner.x, owner.y), (target.x, target.y)) 
        if distance < 2:
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []


class WithinFov:
    """Return success if owner is in the players fov."""
    def tick(self, owner, target, game_map, context):
        if game_map.fov[owner.x, owner.y]:
            return TreeStates.SUCCESS, []
        return TreeStates.FAILURE, []


class WithinL2Radius:
    """Return success if the distance between owner and target is less than or
    equal to some radius.
    """
    def __init__(self, radius):
        self.radius = radius

    def tick(self, owner, target, game_map, context):
        distance = l2_distance((owner.x, owner.y), (target.x, target.y)) 
        if distance <= self.radius: 
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []

class AtLInfinityRadius:
    """Return success if the owner is at exactly a given Linfinity norm
    radius.
    """
    def __init__(self, radius):
        self.radius = radius

    def tick(self, owner, target, game_map, context):
        l_inf_distance = max(abs(owner.x - target.x), abs(owner.y - target.y))
        if l_inf_distance == self.radius:
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []

class CoinFlip:

    def __init__(self, p=0.5):
        self.p = p

    def tick(self, owner, target, game_map, context):
        if random.uniform(0, 1) < self.p:
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []
