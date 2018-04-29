import random


def random_pool(dugeon_floor):
    pinned_room = random.choice(dugeon_floor.rooms)
    pool = Pool(pinned_room)
    pool.seed()
    pool.grow()
    return pool


class Pool:

    def __init__(self, pinned_room):
        self.pinned_room = pinned_room
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
            print(n_attempts)
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
