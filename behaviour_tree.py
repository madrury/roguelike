from enum import Enum, auto

from etc.enum import ResultTypes
from utils.utils import distance_to


class TreeStates(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    RUNNING = auto()


class Sequence:
    """Tick childeren in sequence we encounter a failure.  If no failure is
    encountered, propogate the results of the final child.
    """
    def __init__(self, *children):
        self.children = children

    def tick(self, owner, target, game_map, context):
        for child in self.children:
            state, results = child.tick(owner, target, game_map, context)
            if state == TreeStates.FAILURE:
                return state, results
        return state, results
        

class Selection:
    """Tick chideren in sequence until success and propogate the results of
    that success.  If no success is encuntered, propogate failure.
    """
    def __init__(self, *children):
        self.children = children

    def tick(self, owner, target, game_map, context):
        for child in self.children:
            state, results = child.tick(owner, target, game_map, context)
            if state == TreeStates.SUCCESS:
                return state, results
        return TreeStates.FAILURE, []


class Negate:
    """Tick a single child and return negation of the resulting state."""
    def __init__(self, child):
        self.child = child

    def tick(self, owner, target, game_map, context):
        state, results = self.child.tick(owner, target, game_map, context)
        if state == TreeStates.SUCCESS:
            return TreeStates.FAILURE, results
        elif state == TreeStates.FAILURE:
            return TreeStates.SUCCESS, results
        return state, results


class IsAdjacent:

    def tick(self, owner, target, game_map, context):
        distance = distance_to((owner.x, owner.y), (target.x, target.y)) 
        if distance < 2:
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []


class WithinFov:

    def tick(self, owner, target, game_map, context):
        if game_map.fov[owner.x, owner.y]:
            return TreeStates.SUCCESS, []
        return TreeStates.FAILURE, []


class WithinRadius:

    def __init__(self, radius):
        self.radius = radius

    def tick(self, owner, target, game_map, context):
        distance = distance_to((owner.x, owner.y), (target.x, target.y)) 
        if distance <= self.radius: 
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []


class MoveTowards:

    def tick(self, owner, target, game_map, context):
        results = [{ResultTypes.MOVE_TOWARDS: (owner, target.x, target.y)}]
        return TreeStates.SUCCESS, results


class Skitter:

    def tick(self, owner, target, game_map, context):
        results = [{ResultTypes.MOVE_RANDOM_ADJACENT: owner}]
        return TreeStates.SUCCESS, results


class Attack:

    def tick(self, owner, target, game_map, context):
        if owner.attacker and target.harmable and target.harmable.hp > 0:
            return (TreeStates.SUCCESS,
                    owner.attacker.attack(game_map, target))
        else:
            return TreeStates.FAILURE, []
