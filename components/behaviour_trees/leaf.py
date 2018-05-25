from etc.enum import TreeStates

from pathfinding import get_shortest_path
from etc.enum import ResultTypes
from utils.utils import distance_to, random_walkable_position


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
    """Pick a random position on the map and walk towards it until getting
    there.
    """
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
