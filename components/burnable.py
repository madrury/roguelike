from messages import Message
from etc.enum import ResultTypes, Elements
from etc.colors import COLORS
from etc.config import PROBABILITIES
import spawnable.various


class ItemBurnable:

    def burn(self, game_map):
        fire = spawnable.various.Fire.make(
            game_map, self.owner.x, self.owner.y)
        return [{
            ResultTypes.REMOVE_ENTITY: self.owner,
            ResultTypes.ADD_ENTITY: fire}] 


class AliveBurnable:

    def burn(self, game_map):
        return [{ResultTypes.DAMAGE: (self.owner, 5, Elements.FIRE)}]


class GrassBurnable:

    def __init__(self, p_fire=PROBABILITIES['grass_burn']):
        self.p_fire = p_fire

    def burn(self, game_map):
        game_map.terrain[self.owner.x, self.owner.y] = False
        fire = spawnable.various.Fire.maybe_make(
            game_map, self.owner.x, self.owner.y, p=self.p_fire)
        if fire:
            return [{
                ResultTypes.REMOVE_ENTITY: self.owner,
                ResultTypes.ADD_ENTITY: fire}] 
        else:
            return [{
                ResultTypes.REMOVE_ENTITY: self.owner}]


class WaterBurnable:

    def burn(self, game_map):
        steam = spawnable.various.Steam.make(
            game_map, self.owner.x, self.owner.y)
        if steam:
            return [{ResultTypes.ADD_ENTITY: steam}]
        else:
            return []
