from enum import Enum, auto

from pathfinding import get_shortest_path
from etc.enum import ResultTypes
from utils.utils import distance_to, random_walkable_position



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
    """Return sucess is owner is adjacent to target."""
    def tick(self, owner, target, game_map, context):
        distance = distance_to((owner.x, owner.y), (target.x, target.y)) 
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


class WithinRadius:
    """Return success if the distance between owner and target is less than or
    equal to some radius.
    """
    def __init__(self, radius):
        self.radius = radius

    def tick(self, owner, target, game_map, context):
        distance = distance_to((owner.x, owner.y), (target.x, target.y)) 
        if distance <= self.radius: 
            return TreeStates.SUCCESS, []
        else:
            return TreeStates.FAILURE, []


class MoveTowards:
    """Move the owner towards a target."""
    def tick(self, owner, target, game_map, context):
        results = [{ResultTypes.MOVE_TOWARDS: (owner, target.x, target.y)}]
        return TreeStates.SUCCESS, results


class TravelToRandomPosition:

    def __init__(self):
        self.target_position = None
        self.target_path = None

    def tick(self, owner, target, game_map, context):
        if not self.target_position:
            self.target_position = random_walkable_position(game_map, owner)
        self.path = get_shortest_path(
            game_map,
            (owner.x, owner.y),
            self.target_position,
            routing_avoid=owner.routing_avoid)
        if len(self.path) <= 2:
            self.target_position = None
            return TreeStates.SUCCESS, []
        results = [{
            ResultTypes.MOVE_TOWARDS: (owner, self.path[1][0], self.path[1][1])}]
        return TreeStates.SUCCESS, results


class Skitter:
    """Move the owner to a random adjacent tile."""
    def tick(self, owner, target, game_map, context):
        results = [{ResultTypes.MOVE_RANDOM_ADJACENT: owner}]
        return TreeStates.SUCCESS, results


class Attack:
    """The owner attackes the target."""
    def tick(self, owner, target, game_map, context):
        if owner.attacker and target.harmable and target.harmable.hp > 0:
            return (TreeStates.SUCCESS,
                    owner.attacker.attack(game_map, target))
        else:
            return TreeStates.FAILURE, []
