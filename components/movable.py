import random
from pathfinding import get_shortest_path

from etc.enum import RoutingOptions


class Movable:

    def move(self, game_map, dx, dy):
        x, y = self.owner.x, self.owner.y
        new_x, new_y = x + dx, y + dy
        self.set_position_if_able(game_map, new_x, new_y)

    def move_towards(self, target_x, target_y, game_map):
        path = get_shortest_path(
            game_map, (self.owner.x, self.owner.y), (target_x, target_y),
            routing_avoid=self.owner.routing_avoid)
        if path == []:
            path = get_shortest_path(
                game_map, (self.owner.x, self.owner.y), (target_x, target_y),
                routing_avoid=[])
        if len(path) > 1:
            dx, dy = path[0][0] - self.owner.x, path[0][1] - self.owner.y
            self.move(game_map, dx, dy)

    def move_to_random_adjacent(self, game_map):
        dx, dy = random.choice([
            (-1, 1), (0, 1), (1, 1),
            (-1, 0),         (1, 0),
            (-1, -1), (0, -1), (1, -1)])
        self.move(game_map, dx, dy)

    def set_position_if_able(self, game_map, x, y):
        target_location = (x, y)
        is_walkable = game_map.walkable[target_location]
        is_blocked = game_map.blocked[target_location]
        # Logically equivelent to: if space is water => entity does not avoid water
        water_if_able = (RoutingOptions.AVOID_WATER not in self.owner.routing_avoid
                         or not game_map.water[target_location])
        if is_walkable and not is_blocked and water_if_able:
            if self.owner.blocks:
                game_map.blocked[self.owner.x, self.owner.y] = False
                game_map.blocked[target_location] = True
            game_map.entities.update_position(
                self.owner, (self.owner.x, self.owner.y), target_location)
            self.owner.x, self.owner.y = target_location 
