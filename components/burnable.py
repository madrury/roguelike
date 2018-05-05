from messages import Message
from etc.enum import ResultTypes
from etc.colors import COLORS
from etc.config import PROBABILITIES
from spawnable.various import Fire


class GrassBurnable:

    def __init__(self, p_fire=PROBABILITIES['grass_burn']):
        self.p_fire = p_fire

    def burn(self, game_map):
        game_map.terrain[self.owner.x, self.owner.y] = False
        fire = Fire.maybe_make(
            game_map, self.owner.x, self.owner.y, p=self.p_fire)
        if fire:
            return [{
                ResultTypes.REMOVE_ENTITY: self.owner,
                ResultTypes.ADD_ENTITY: fire}] 
        else:
            return [{
                ResultTypes.REMOVE_ENTITY: self.owner}]
