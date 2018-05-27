from etc.enum import ResultTypes, Elements
import game_objects.terrain


class ShrubEncroachable:

    def encroach(self, game_map, encroacher):
        results = []
        grass = game_objects.terrain.Grass.make(
            game_map, self.owner.x, self.owner.y)
        results.append({ResultTypes.ADD_ENTITY: grass})
        results.append({ResultTypes.REMOVE_ENTITY: self.owner})
        return results


class NecroticSoilEncroachable:

    # TODO: Move to config.
    def __init__(self, damage=2):
        self.damage = damage

    def encroach(self, game_map, encroacher):
        results = []
        results.append({ResultTypes.DAMAGE: (
            encroacher, None, self.damage, Elements.NECROTIC)})
        return results
