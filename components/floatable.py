from utils.utils import random_adjacent
from etc.enum import ResultTypes


class Floatable:
    """Component for floating an entity idly in water."""
    def float(self, game_map):
        x, y = self.owner.x, self.owner.y
        coord = random_adjacent((x, y))
        if game_map.walkable[coord[0], coord[1]]:
            return [{ResultTypes.SET_POSITION: (
                self.owner, coord[0], coord[1])}]
        return []
