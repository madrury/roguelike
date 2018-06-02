from etc.enum import ResultTypes, Elements
from etc.game_config import NECROTIC_SOIL_BASE_DAMAGE
import game_objects.terrain


class ShrubEncroachable:
    """When an entity encroaches on a shrub, the shrub is trampled into
    grass.
    """
    def encroach(self, game_map, encroacher):
        results = []
        grass = game_objects.terrain.Grass.make(
            game_map, self.owner.x, self.owner.y)
        results.append({ResultTypes.ADD_ENTITY: grass})
        results.append({ResultTypes.REMOVE_ENTITY: self.owner})
        return results


class NecroticSoilEncroachable:
    """When an entity encroaches on necrotic soul, the soil does necrotic
    damage to the entity.
    """
    def __init__(self, damage=NECROTIC_SOIL_BASE_DAMAGE):
        self.damage = damage

    def encroach(self, game_map, encroacher):
        results = []
        if encroacher.harmable:
            results.append({ResultTypes.DAMAGE: (
                encroacher, None, self.damage, [Elements.NECROTIC])})
        return results
