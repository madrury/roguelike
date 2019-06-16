"""
Components governing state changes when an entity is committed to the game map.

The game map has internal state that tracks where enitites are located.  When
entities are added and remove from the map, this state must be updated.  This
component governs this logic for each type of entity, which differs by type of entity.

For example:

  - Some entities block movement into the square in which they are located.
  - Some entities block line of sight.

Etc.
"""

# TODO: These methods should return True of False to signal if they are successful.

class BaseCommitable:
    """Baseline logic for commiting a new entity to the map."""
    def commit(self, game_map):
        game_map.entities.append(self.owner)

    def delete(self, game_map):
        if self.owner in game_map.entities:
            game_map.entities.remove(self.owner)


class BlockingCommitable:
    """Commit or delete a blocking entity to/from the game map."""
    def commit(self, game_map):
        if game_map.blocked[self.owner.x, self.owner.y]:
            # LOG: Log message.
            return
        else:
            game_map.blocked[self.owner.x, self.owner.y] = True
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        x, y = self.owner.x, self.owner.y
        if not game_map.blocked[x, y]:
            raise RuntimeError(
                f"Attempt to remove blocking entity {self.owner} from "
                f"unblocked space {x}, {y}.")
        game_map.blocked[self.owner.x, self.owner.y] = False
        game_map.entities.remove(self.owner)


class DoorCommitable:

    def commit(self, game_map):
        game_map.transparent[self.owner.x, self.owner.y] = False
        game_map.door[self.owner.x, self.owner.y] = True
        game_map.entities.append(self.owner)

    def delete(self, game_map):
        game_map.transparent[self.owner.x, self.owner.y] = True
        game_map.door[self.owner.x, self.owner.y] = False
        game_map.entities.remove(self.owner)


class FireCommitable:

    def commit(self, game_map):
        if game_map.fire[self.owner.x, self.owner.y]:
            return
        else:
            game_map.fire[self.owner.x, self.owner.y] = True
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        if not game_map.fire[self.owner.x, self.owner.y]:
            raise RuntimeError(
                f"Attempt to remove fire entity {self.owner} from "
                 "non-fire space.")
        game_map.fire[self.owner.x, self.owner.y] = False
        game_map.entities.remove(self.owner)


class SteamCommitable:

    def commit(self, game_map):
        if game_map.steam[self.owner.x, self.owner.y]:
            return
        else:
            game_map.steam[self.owner.x, self.owner.y] = True
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        if not game_map.steam[self.owner.x, self.owner.y]:
            raise RuntimeError(
                f"Attempt to remove steam entity {self.owner} from "
                 "non-steam space.")
        game_map.steam[self.owner.x, self.owner.y] = False
        game_map.entities.remove(self.owner)


class TerrainCommitable:

    def commit(self, game_map):
        if game_map.terrain[self.owner.x, self.owner.y]:
            return
        else:
            game_map.terrain[self.owner.x, self.owner.y] = True
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        x, y = self.owner.x, self.owner.y
        if self.owner in game_map.entities:
            # TODO: This is inside the above check because in certain
            # circumstances, a terrain entity will be removed from the map
            # twice.  For example, if two different fires attempt to burn the
            # same patch of grass, two signals will be sent to remove it from
            # the map.  There may be a more transparant way to handle this.
            if not game_map.terrain[self.owner.x, self.owner.y]:
                raise RuntimeError(
                    f"Attempt to remove terrain entity {self.owner.name} from "
                    f"non-terrain space {x}, {y}.")
            game_map.terrain[self.owner.x, self.owner.y] = False
            game_map.entities.remove(self.owner)


class BlockingTerrainCommitable:

    def commit(self, game_map):
        if not (game_map.terrain[self.owner.x, self.owner.y]
            and not game_map.blocked[self.owner.x, self.owner.y]):
            game_map.blocked[self.owner.x, self.owner.y] = True
            game_map.terrain[self.owner.x, self.owner.y] = True
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        x, y = self.owner.x, self.owner.y
        if self.owner in game_map.entities:
            # TODO: This is inside the above check because in certain
            # circumstances, a terrain entity will be removed from the map
            # twice.  For example, if two different fires attempt to burn the
            # same patch of grass, two signals will be sent to remove it from
            # the map.  There may be a more transparant way to handle this.
            if not game_map.terrain[x, y]:
                raise RuntimeError(
                    f"Attempt to remove terrain entity {self.owner.name} from "
                    f"non-terrain space {x}, {y}.")
            if not game_map.blocked[self.owner.x, self.owner.y]:
                raise RuntimeError(
                    f"Attempt to remove blocking entity {self.owner.name} from "
                    "unblocked space {x}, {y}.")
            game_map.terrain[self.owner.x, self.owner.y] = False
            game_map.entities.remove(self.owner)


class UpwardStairsCommitable:

    def commit(self, game_map):
        if not game_map.terrain[self.owner.x, self.owner.y]:
            game_map.terrain[self.owner.x, self.owner.y] = True
            game_map.walkable[self.owner.x, self.owner.y] = True
            game_map.upward_stairs_position = (self.owner.x, self.owner.y)
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        if self.owner in game_map.entities:
            raise RuntimeError("Stairs cannot be deleted from the game map.")


class DownwardStairsCommitable:

    def commit(self, game_map):
        if not game_map.terrain[self.owner.x, self.owner.y]:
            game_map.terrain[self.owner.x, self.owner.y] = True
            game_map.walkable[self.owner.x, self.owner.y] = True
            game_map.downward_stairs_position = (self.owner.x, self.owner.y)
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        if self.owner in game_map.entities:
            raise RuntimeError("Stairs cannot be deleted from the game map.")


class WaterCommitable:
    # TODO: This in unsafe, need more stringent checks.
    def commit(self, game_map):
        if not game_map.terrain[self.owner.x, self.owner.y]:
            game_map.terrain[self.owner.x, self.owner.y] = True
            game_map.water[self.owner.x, self.owner.y] = True
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        if self.owner in game_map.entities:
            game_map.terrain[self.owner.x, self.owner.y] = False
            game_map.water[self.owner.x, self.owner.y] = False
            game_map.entities.remove(self.owner)


class IceCommitable:

    def commit(self, game_map):
        if not game_map.terrain[self.owner.x, self.owner.y]:
            game_map.terrain[self.owner.x, self.owner.y] = True
            game_map.ice[self.owner.x, self.owner.y] = True
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        if self.owner in game_map.entities:
            game_map.terrain[self.owner.x, self.owner.y] = False
            game_map.ice[self.owner.x, self.owner.y] = False
            game_map.entities.remove(self.owner)


class ShrubCommitable(TerrainCommitable):

    def commit(self, game_map):
        super().commit(game_map)
        game_map.transparent[self.owner.x, self.owner.y] = False
        game_map.shrub[self.owner.x, self.owner.y] = True

    def delete(self, game_map):
        super().delete(game_map)
        game_map.transparent[self.owner.x, self.owner.y] = True
        game_map.shrub[self.owner.x, self.owner.y] = False