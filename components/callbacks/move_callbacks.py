from etc.enum import ResultTypes
from etc.game_config import RAIPIER_RANGE

from utils.utils import get_blocking_entity_in_position


class RaipierCallback:

    def execute(self, game_map, owner, destination):
        dx, dy = destination[0] - owner.x, destination[1] - owner.y 
        path = [(owner.x + i*dx, owner.y + i*dy) for i in range(RAIPIER_RANGE)]
        prior_coord = (owner.x, owner.y)
        for x, y in path[1:]:
            if not game_map.walkable[x, y]:
                break
            target = get_blocking_entity_in_position(game_map, (x, y))
            if target:
                break
            prior_coord = (x, y)
        results = []
        if target:
            results.extend(owner.attacker.attack(game_map, target))
            results.append({
                ResultTypes.SET_POSITION: (
                    owner, prior_coord[0], prior_coord[1])})
        else:
            results.append({
                # TODO: This assumes the player is moving, which is hardcoded
                # in the game loop.  We shoud be able to handle a generic move.
                ResultTypes.MOVE: (dx, dy),
                ResultTypes.END_TURN: True})
        return results
