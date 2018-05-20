from etc.enum import ResultTypes
import game_objects.terrain


class ShrubEncroachable:

    def encroach(self, game_map, encroacher):
        results = []
        grass = game_objects.terrain.Grass.make(
            game_map, self.owner.x, self.owner.y)
        results.append({ResultTypes.ADD_ENTITY: grass})
        results.append({ResultTypes.REMOVE_ENTITY: self.owner})
        return results
