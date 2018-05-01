import random
from etc.enum import Terrain
from utils.utils import adjacent_coordinates


def add_random_terrain(game_map):
    min_pools, max_pools = 2, 8
    floor = game_map.floor
    n_pools = random.randint(min_pools, max_pools)
    for _ in range(n_pools):
        pool = random_pool(game_map)
        floor.pools.append(pool)
        pool.write_to_game_map()
    river = random_river(game_map)
    river.write_to_game_map()


def random_pool(game_map):
    pinned_room = random.choice(game_map.floor.rooms)
    pool = Pool(game_map, pinned_room)
    pool.seed()
    pool.grow()
    return pool


class Pool:

    def __init__(self, game_map, room):
        self.game_map = game_map
        self.room = room
        room.terrain = Terrain.POOL
        self.coords = []

    def __iter__(self):
        yield from iter(self.coords)

    def write_to_game_map(self):
        for x, y in self:
            self.game_map.pool[x, y] = True
            self.game_map.make_transparent_and_walkable(x, y)

    def seed(self):
        coord = self.room.random_point()
        self.coords.append(coord)

    def grow(self, n_attempts=None):
        if not n_attempts:
            n_attempts = int(0.7 * self.room.room.width * self.room.room.height)
        self.seed()
        for i in range(n_attempts):
            coord = random.choice(self.coords)
            x, y = self.grow_one(coord)
            if self.game_map.within_bounds(x, y):
                self.coords.append([x, y])
            else:
                print(x, y, self.game_map.within_bounds(x, y))

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

    def __init__(self, game_map, source_room, dest_room, width=1):
        self.game_map = game_map
        self.source_point = self.get_random_pool_point(source_room)
        self.dest_point = self.get_random_pool_point(dest_room)
        self.coords = set(game_map.compute_path(
            self.source_point[0], self.source_point[1],
            self.dest_point[0], self.dest_point[1]))
        self.grow(width)

    def write_to_game_map(self):
        for x, y in self.coords:
            self.game_map.pool[x, y] = True
            self.game_map.make_transparent_and_walkable(x, y)

    def grow(self, width):
        for _ in range(width - 1):
            new_coords = set()
            for river_coord in self.coords:
                for coord in adjacent_coordinates(river_coord):
                    new_coords.add(coord)
            self.coords.update(new_coords)

    def get_random_pool_point(self, room):
        if room.terrain != Terrain.POOL:
            raise ValueError("Cannot create river in room with no pool tiles.")
        x, y = room.random_point()
        while not self.game_map.pool[x, y]:
            x, y = room.random_point()
        return x, y
