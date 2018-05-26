import random
from pathfinding import get_shortest_path


class Movable:

    def set_position(self, game_map, x, y):
        if self.owner.blocks:
            game_map.blocked[self.owner.x, self.owner.y] = False
            game_map.blocked[x, y] = True
        self.owner.x, self.owner.y = x, y

    def move(self, game_map, dx, dy):
        x, y = self.owner.x, self.owner.y
        new_x, new_y = x + dx, y + dy
        if self.owner.blocks:
            game_map.blocked[x, y] = False
            game_map.blocked[new_x, new_y] = True
        self.owner.x += dx
        self.owner.y += dy

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
            self._move_if_able(dx, dy, game_map)

    def move_to_random_adjacent(self, game_map):
        dx, dy = random.choice([
            (-1, 1), (0, 1), (1, 1),
            (-1, 0),         (1, 0),
            (-1, -1), (0, -1), (1, -1)])
        self._move_if_able(dx, dy, game_map)

    def _move_if_able(self, dx, dy, game_map):
        target_location = (self.owner.x + dx, self.owner.y + dy)
        is_walkable = game_map.walkable[target_location]
        is_blocked = game_map.blocked[target_location]
        water_if_able = self.owner.swimmable or not game_map.water[target_location]
        if is_walkable and not is_blocked and water_if_able:
            self.move(game_map, dx, dy)
