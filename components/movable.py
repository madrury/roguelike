import random
from pathfinding import get_shortest_path

from etc.enum import RoutingOptions


class Movable:
    """Handle movement of entities."""

    def set_position_if_able(self, game_map, x, y):
        """Set the position of the owner to a given postition.
        
        This is the lowest level method for manipulating an entities positon on
        the mpd, and as such, it checks if the resulting positon is actually
        valid to hold the owner.

          - Is the proposed new positon walkable?
          - Is the proposed new position blocked?
          - If the owner cannot reside in water, is the proposed new positon water?

        If all the checks pass, the position of the entity is set to the
        proposed positon, the blocked array of the game map is updated, and the
        position of the entity within the entity array is updated.

        Returns True or False, depending on if the new position was set.
        """
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
            return True
        return False

    def move(self, game_map, dx, dy):
        """Attempt to move the owner in a given direction (dx, dy).
        
        The basic behaviour here is to set the position to (x + dx, y + dy).
        This behaviour is overrode if the player is attempting to move onto
        ice, in which case the owner slides an additional space in that
        direction.
        """
        x, y = self.owner.x, self.owner.y
        is_ice = game_map.ice[x + dx, y + dy]
        success = False
        if is_ice:
            new_x, new_y = x + 2*dx, y + 2*dy
            success = self.set_position_if_able(game_map, new_x, new_y)
        if not success:
            new_x, new_y = x + dx, y + dy
            self.set_position_if_able(game_map, new_x, new_y)

    def move_towards(self, target_x, target_y, game_map):
        """Move the owner one step towards a target."""
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
        """Move the owner to a random adjacent tile."""
        dx, dy = random.choice([
            (-1, 1), (0, 1), (1, 1),
            (-1, 0),         (1, 0),
            (-1, -1), (0, -1), (1, -1)])
        self.set_position_if_able(game_map, self.owner.x + dx, self.owner.y + dy)
