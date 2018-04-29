import random
from etc.enum import Terrain


def random_pool(dugeon_floor):
    pinned_room = random.choice(dugeon_floor.rooms)
    pool = Pool(pinned_room)
    pool.seed()
    pool.grow()
    return pool


class Pool:

    def __init__(self, pinned_room):
        self.pinned_room = pinned_room
        pinned_room.terrain = Terrain.POOL
        self.room = pinned_room.room
        self.coords = []

    def __iter__(self):
        for x, y in self.coords:
            yield x + self.pinned_room.x, y + self.pinned_room.y

    def write_to_game_map(self, game_map):
        for x, y in self:
            game_map.pool[x, y] = True

    def seed(self):
        coord = self.room.random_point()
        self.coords.append(coord)

    def grow(self, n_attempts=None):
        if not n_attempts:
            n_attempts = int((3/2) * self.room.width * self.room.height)
        self.seed()
        for i in range(n_attempts):
            coord = random.choice(self.coords)
            new_coord = self.grow_one(coord)
            if new_coord in self.room:
                self.coords.append(new_coord)
        return self

    def grow_one(self, coord):
        x, y = coord
        candidates = [
            (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
            (x - 1, y),                 (x + 1, y),
            (x - 1, y - 1), (x, y - 1), (x + 1, y + 1)]
        return random.choice(candidates)


def random_river(game_map):
    r1 = random.choice(game_map.floor.rooms)
    while r1.terrain != Terrain.POOL:
        r1 = random.choice(game_map.floor.rooms)
    r2 = random.choice(game_map.floor.rooms)
    while r1 == r2 or r2.terrain != Terrain.POOL:
        r2 = random.choice(game_map.floor.rooms)
    river = River(game_map, r1, r2)
    return river

class River:

    def __init__(self, game_map, source_room, dest_room):
        self.game_map = game_map
        self.source_point = self.get_random_pool_point(source_room)
        self.dest_point = self.get_random_pool_point(dest_room)
        self.path = game_map.compute_path(
            self.source_point[0], self.source_point[1],
            self.dest_point[0], self.dest_point[1])

    def write_to_game_map(self):
        for x, y in self.path:
            self.game_map.pool[x, y] = True

    def get_random_pool_point(self, room):
        if room.terrain != Terrain.POOL:
            raise ValueError("Cannot create river in room with no pool tiles.")
        x, y = room.random_point()
        while not self.game_map.pool[x, y]:
            x, y = room.random_point()
        return x, y
