class BaseCommitable:

    def commit(self, game_map):
        game_map.entities.append(self.owner)

    def delete(self, game_map):
        if self.owner in game_map.entities:
            game_map.entities.remove(self.owner)


class BlockingCommitable:

    def commit(self, game_map):
        if game_map.blocked[self.owner.x, self.owner.y]:
            return
        else:
            game_map.blocked[self.owner.x, self.owner.y] = True
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        if not game_map.blocked[self.owner.x, self.owner.y]:
            raise RuntimeError(
                f"Attempt to remove blocking entity {self.owner} from "
                 "unblocked space.")
        game_map.blocked[self.owner.x, self.owner.y] = False
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
        if not game_map.terrain[self.owner.x, self.owner.y]:
            game_map.terrain[self.owner.x, self.owner.y] = True
            game_map.entities.append(self.owner)

    def delete(self, game_map):
        if self.owner in game_map.entities:
            game_map.terrain[self.owner.x, self.owner.y] = False
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

