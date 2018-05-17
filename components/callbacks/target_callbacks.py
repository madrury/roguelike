from entity import get_blocking_entity_at_location
from utils.utils import adjacent_coordinates

class LanceCallback:

    def execute(self, game_map, target, source):
        dx, dy = target.x - source.x, target.y - source.y
        targets = [target]
        if game_map.within_bounds(target.x + dx, target.y + dy):
            new_target = get_blocking_entity_at_location(
                game_map, target.x + dx, target.y + dy)
            if new_target:
                targets.append(new_target)
        if game_map.within_bounds(target.x + 2*dx, target.y + 2*dy):
            new_target = get_blocking_entity_at_location(
                game_map, target.x + 2*dx, target.y + 2*dy)
            if new_target:
                targets.append(new_target)
        return targets

class AxeCallback:

    def execute(self, game_map, target, source):
        adj = adjacent_coordinates((source.x, source.y))
        targets = []
        for x, y in adj:
            if game_map.within_bounds(x, y):
                target = get_blocking_entity_at_location(game_map, x, y)
                if target:
                    targets.append(target)
        return targets
