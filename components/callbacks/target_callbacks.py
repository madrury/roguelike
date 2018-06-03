from utils.utils import adjacent_coordinates, get_blocking_entity_in_position

class LanceCallback:
    """A lance targets the tree spaces in a line as long as there is an
    adjacent entity to be targeted.
    """
    def execute(self, game_map, target, source):
        dx, dy = target.x - source.x, target.y - source.y
        targets = [target]
        if game_map.within_bounds(target.x + dx, target.y + dy):
            new_target = get_blocking_entity_in_position(
                game_map, (target.x + dx, target.y + dy))
            if new_target:
                targets.append(new_target)
        if game_map.within_bounds(target.x + 2*dx, target.y + 2*dy):
            new_target = get_blocking_entity_in_position(
                game_map, (target.x + 2*dx, target.y + 2*dy))
            if new_target:
                targets.append(new_target)
        return targets


class SwordCallback:
    """A sword targets all spaces in a three space arc adjacent to the player
    and centered at the target's space.
    """
    def execute(self, game_map, target, source):
        target_coordinates = self.get_target_coordinates(target, source)
        print((source.x, source.y), target_coordinates)
        targets = []
        for coord in target_coordinates:
            target = get_blocking_entity_in_position(game_map, coord)
            if target:
                targets.append(target)
        return targets

    def get_target_coordinates(self, target, source):
        reverse_x, reverse_y = False, False
        dx, dy = target.x - source.x, target.y - source.y
        print(dx, dy)
        if dx < 0:
            reverse_x, dx = True, -dx
        if dy < 0:
            reverse_y, dy = True, -dy
        if (dx, dy) == (1, 1):
            dtargets = [(0, 1), (1, 1), (1, 0)]
        if (dx, dy) == (0, 1):
            dtargets = [(-1, 1), (0, 1), (1, 1)]
        if (dx, dy) == (1, 0):
            dtargets = [(1, -1), (1, 0), (1, 1)]
        print(dtargets)
        if reverse_x:
            dtargets = [(-dx, dy) for dx, dy in dtargets]
        if reverse_y:
            dtargets = [(dx, -dy) for dx, dy in dtargets]
        return [(source.x + dx, source.y + dy) for (dx, dy) in dtargets]


class AxeCallback:
    """An axe targets all adjacent spaces as long as there is an adjacent
    entity to be targeted.
    """
    def execute(self, game_map, target, source):
        adj = adjacent_coordinates((source.x, source.y))
        targets = []
        for x, y in adj:
            if game_map.within_bounds(x, y):
                target = get_blocking_entity_in_position(game_map, (x, y))
                if target:
                    targets.append(target)
        return targets
