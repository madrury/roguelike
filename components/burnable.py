from messages import Message
from etc.enum import ResultTypes, Elements
from etc.colors import COLORS
from etc.game_config import GRASS_BURN_PROBABILTY, BURN_BASE_DAMAGE
import game_objects.various
import game_objects.terrain


class ItemBurnable:
    """Items are destroyed when they burn, and spawn fire."""
    def burn(self, game_map):
        fire = game_objects.various.Fire.make(
            game_map, self.owner.x, self.owner.y)
        return [{
            ResultTypes.REMOVE_ENTITY: self.owner,
            ResultTypes.ADD_ENTITY: fire}] 


class AliveBurnable:
    """A living creature takes fire elemental damage from a fire."""
    def burn(self, game_map):
        return [{ResultTypes.DAMAGE: (
            self.owner, None, BURN_BASE_DAMAGE, [Elements.FIRE])}]


class ZombieBurnable:
    """Imediately kill the zombie and spawn a fire in their space."""
    def burn(self, game_map):
        fire = game_objects.various.Fire.make(
            game_map, self.owner.x, self.owner.y)
        return [{
            ResultTypes.ADD_ENTITY: fire,
            ResultTypes.DEAD_ENTITY: self.owner}]


class WaterBloatBurnable:
    """Spawn steam and deal fire damage."""
    def burn(self, game_map):
        results = [] 
        steam = game_objects.various.Steam.make(
            game_map, self.owner.x, self.owner.y)
        results.append({ResultTypes.ADD_ENTITY: steam})
        # This is enough damage to immediately kill a bloat.
        results.append({ResultTypes.DAMAGE: (
            self.owner, None, 1, [Elements.FIRE])})
        return results


class GrassBurnable:
    """When grass burns, the grass entity is removed from the game and
    (sometimes) replaced with a fire entity.
    
    Grass does not alway burn, it only catched fire with a fixed probability.
    """
    def __init__(self, p_fire=GRASS_BURN_PROBABILTY):
        self.p_fire = p_fire

    def burn(self, game_map):
        fire = game_objects.various.Fire.maybe_make(
            game_map, self.owner.x, self.owner.y, p=self.p_fire)
        burned_grass = game_objects.terrain.BurnedGrass.maybe_make(
            game_map, self.owner.x, self.owner.y)
        results = []
        # The order of events here is important.  We need to remove the terrain
        # entity (grass) from the tile before adding the new terrain (burned
        # grass), since each tile can only hold one terrain.
        if burned_grass:
            results.append({ResultTypes.ADD_ENTITY: burned_grass})
        if fire:
            results.append({ResultTypes.ADD_ENTITY: fire})
        results.append({ResultTypes.REMOVE_ENTITY: self.owner})        
        return results


class WaterBurnable:
    """When water burns, it spawns a steam entity within the same square."""
    def burn(self, game_map):
        steam = game_objects.various.Steam.make(
            game_map, self.owner.x, self.owner.y)
        if steam:
            return [{ResultTypes.ADD_ENTITY: steam}]
        else:
            return []


class IceBurnable:
    """When ice is burned, it melts, leaving behind water."""
    def burn(self, game_map):
        water = game_objects.terrain.Water.make(
            game_map, self.owner.x, self.owner.y)
        if water:
            return [{
                ResultTypes.ADD_ENTITY: water,
                ResultTypes.REMOVE_ENTITY: self.owner}]
        else:
            return []
