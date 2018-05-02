import random

from entity import Entity
from etc.enum import Terrain, EntityTypes, RenderOrder
from etc.colors import COLORS
from utils.utils import adjacent_coordinates, random_adjacent


def add_random_terrain(game_map, entities, terrain_config):
    floor = game_map.floor
    min_pools, max_pools = (
        terrain_config['min_pools'], terrain_config['max_pools'])
    pool_room_proportion = terrain_config['pool_room_proportion']
    n_pools = random.randint(min_pools, max_pools)
    for _ in range(n_pools):
        pool = random_pool(game_map, 
                           pool_room_proportion=pool_room_proportion)
        floor.pools.append(pool)
        pool.write_to_game_map()

    min_rivers, max_rivers = (
        terrain_config['min_rivers'], terrain_config['max_rivers'])
    n_rivers = random.randint(min_rivers, max_rivers)
    for _ in range(n_rivers):
        river = random_river(game_map)
        river.write_to_game_map()

    grass = random_grass(game_map)
    entities.extend(grass.get_entities())



class Growable:

    def __init__(self, game_map, room):
        self.game_map = game_map
        self.room = room
        self.coords = []

    def __iter__(self):
        yield from iter(self.coords)

    def seed(self):
        coord = self.room.random_point()
        self.coords.append(coord)

    def grow(self, stay_in_room=False, proportion=None, n_attempts=None):
        if not n_attempts:
            n_attempts = int(
                proportion * self.room.width * self.room.height)
        self.seed()
        for i in range(n_attempts):
            coord = random.choice(self.coords)
            x, y = random_adjacent(coord)
            is_valid = (not stay_in_room or self.game_map.walkable[x, y])
            if is_valid and self.game_map.within_bounds(x, y, buffer=1):
                self.coords.append([x, y])

#-----------------------------------------------------------------------------
# Pool
#-----------------------------------------------------------------------------
def random_pool(game_map, pool_room_proportion):
    pinned_room = random.choice(game_map.floor.rooms)
    while pinned_room.terrain != None:
        pinned_room = random.choice(game_map.floor.rooms)
    pool = Pool(game_map, pinned_room)
    pool.seed()
    pool.grow(stay_in_room=False,
              proportion=pool_room_proportion)
    return pool


class Pool(Growable):

    def __init__(self, game_map, room):
        super().__init__(game_map, room)
        room.terrain = Terrain.POOL


    def write_to_game_map(self):
        for x, y in self:
            self.game_map.pool[x, y] = True
            self.game_map.make_transparent_and_walkable(x, y)


#-----------------------------------------------------------------------------
# Grass
#-----------------------------------------------------------------------------
class Grass(Growable):

    def __init__(self, game_map, room):
        super().__init__(game_map, room)
        room.terrain = Terrain.GRASS
        
    def get_entities(self):
        return [self.make(x, y) for x, y in self]

    @staticmethod
    def make(x, y):
        return Entity(
            x, y, '"',
            name="Grass",
            fg_color=COLORS['light_grass'],
            dark_fg_color=COLORS['dark_grass'],
            visible_out_of_fov=True,
            entity_type=EntityTypes.TERRAIN,
            render_order=RenderOrder.TERRAIN)


def random_grass(game_map):
    pinned_room = random.choice(game_map.floor.rooms)
    while pinned_room.terrain != None:
        pinned_room = random.choice(game_map.floor.rooms)
    grass = Grass(game_map, pinned_room)
    grass.grow(stay_in_room=True, proportion=1.5)
    return grass
    

#-----------------------------------------------------------------------------
# River
#-----------------------------------------------------------------------------
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

    def grow(self, width=1):
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
