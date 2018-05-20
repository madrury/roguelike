from etc.enum import ResultTypes


class ShrubEncroachable:

    def encroach(self, encroacher, game_map):
        results = []
        grass = Grass.make(game_map, self.owner.x, self.owner.y)
        results.append({ResultTypes.ADD_ENTITY: grass})
        results.append({ResultTypes.REMOVE_ENTITY: self.owner})
        return results
