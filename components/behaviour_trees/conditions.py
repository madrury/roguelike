import random

from utils.utils import l2_distance
from etc.enum import TreeStates
from components.behaviour_trees.root import Node


class InNamespace(Node):
    """Check if a variable is set within the tree's namespace.
    
    Attributes
    ----------
    name: str
      The name of the variable in the tree's namespace.
    """
    def __init__(self, name):
        self.name = name

    def tick(self, owner, game_map):
        if self.namespace.get(self.name):
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []


class IsAdjacent(Node):
    """Return sucess is owner is adjacent to target."""
    def tick(self, owner, game_map):
        target = self.namespace.get("target")
        distance = l2_distance((owner.x, owner.y), (target.x, target.y)) 
        if distance < 2:
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []


class WithinFov(Node):
    """Return success if owner is in the player's fov."""
    def tick(self, owner, game_map):
        if game_map.fov[owner.x, owner.y]:
            return TreeStates.SUCCESS, []
        return TreeStates.FAILURE, []


class WithinL2Radius(Node):
    """Return success if the distance between owner and target is less than or
    equal to some radius.
    """
    def __init__(self, radius):
        self.radius = radius

    def tick(self, owner, game_map):
        target = self.namespace.get("target")
        distance = l2_distance((owner.x, owner.y), (target.x, target.y)) 
        if distance <= self.radius: 
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []


class AtLInfinityRadius(Node):
    """Return success if the owner is at exactly a given Linfinity norm
    radius.
    """
    def __init__(self, radius):
        self.radius = radius

    def tick(self, owner, game_map):
        target = self.namespace.get("target")
        l_inf_distance = max(abs(owner.x - target.x), abs(owner.y - target.y))
        if l_inf_distance == self.radius:
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []


class CoinFlip(Node):

    def __init__(self, p=0.5):
        self.p = p

    def tick(self, owner, game_map):
        if random.uniform(0, 1) < self.p:
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []
