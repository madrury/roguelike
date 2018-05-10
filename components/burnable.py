from messages import Message
from etc.enum import ResultTypes, Elements
from etc.colors import COLORS
from etc.config import PROBABILITIES
import spawnable.various


class ItemBurnable:
    """Items are destroyed when they burn, and spawn fire."""
    def burn(self, game_map):
        fire = spawnable.various.Fire.make(
            game_map, self.owner.x, self.owner.y)
        return [{
            ResultTypes.REMOVE_ENTITY: self.owner,
            ResultTypes.ADD_ENTITY: fire}] 


class AliveBurnable:
    """A living creature takes fire elemental damage from a fire."""
    # TODO: Move to config.py
    def burn(self, game_map):
        return [{ResultTypes.DAMAGE: (self.owner, 5, Elements.FIRE)}]


class GrassBurnable:
    """When grass burns, the grass entity is removed from the game and replaced
    with a fire entity.
    
    Grass does not alway burn, it only catched fire with a fixed probability.
    """
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
    """When water burns, it spawns a steam entity within the same square."""
    def burn(self, game_map):
        steam = spawnable.various.Steam.make(
            game_map, self.owner.x, self.owner.y)
        if steam:
            return [{ResultTypes.ADD_ENTITY: steam}]
        else:
            return []
