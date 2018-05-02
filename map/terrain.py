import random

from entity import Entity
from colors import random_light_green, random_light_water, random_dark_water
from etc.enum import Terrain, EntityTypes, RenderOrder
from etc.colors import COLORS
from utils.utils import adjacent_coordinates, random_adjacent
from components.shimmer import WaterShimmer
from components.burnable import GrassBurnable


def add_random_terrain(game_map, entities, terrain_config):
    floor = game_map.floor
    min_pools, max_pools = (
        terrain_config['min_pools'], terrain_config['max_pools'])
    pool_room_proportion = terrain_config['pool_room_proportion']
    n_pools = random.randint(min_pools, max_pools)
    for _ in range(n_pools):
        pool = random_pool(game_map, 
                           pool_room_proportion=pool_room_proportion)
        pool.write_to_game_map()
        entities.extend(pool.get_entities())

    min_rivers, max_rivers = (
        terrain_config['min_rivers'], terrain_config['max_rivers'])
    n_rivers = random.randint(min_rivers, max_rivers)
    for _ in range(n_rivers):
        river = random_river(game_map)
        river.write_to_game_map()
        entities.extend(river.get_entities())

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
            is_valid = not stay_in_room or self.game_map.walkable[x, y]
            if is_valid and self.game_map.within_bounds(x, y, buffer=1):
                self.coords.append([x, y])

    def get_entities(self):
        return [self.make(x, y) for x, y in self]

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

def make_water_entity(x, y):
    fg_color = random_light_water()
    bg_color = random_light_water()
    dark_fg_color = random_dark_water()
    dark_bg_color = random_dark_water()
    return Entity(
        x, y, '~',
        name="Water",
        fg_color=fg_color,
        dark_fg_color=dark_fg_color,
        bg_color=bg_color,
        dark_bg_color=dark_bg_color,
        visible_out_of_fov=True,
        entity_type=EntityTypes.TERRAIN,
        render_order=RenderOrder.TERRAIN,
        shimmer=WaterShimmer())


class Pool(Growable):

    def __init__(self, game_map, room):
        super().__init__(game_map, room)
        room.terrain = Terrain.POOL


    def write_to_game_map(self):
        for x, y in self:
            self.game_map.pool[x, y] = True
            self.game_map.make_transparent_and_walkable(x, y)

    @staticmethod
    def make(x, y):
        return make_water_entity(x, y)


#-----------------------------------------------------------------------------
# Grass
#-----------------------------------------------------------------------------
class Grass(Growable):

    def __init__(self, game_map, room):
        super().__init__(game_map, room)
        room.terrain = Terrain.GRASS
        
    @staticmethod
    def make(x, y):
        fg_color = random_light_green()
        # Shift down the green component to make the grass dark.
        bg_color = (fg_color[0], fg_color[1] - 60, fg_color[2])
        return Entity(
            x, y, '"',
            name="Grass",
            fg_color=fg_color,
            dark_fg_color=bg_color,
            visible_out_of_fov=True,
            entity_type=EntityTypes.TERRAIN,
            render_order=RenderOrder.TERRAIN,
            burnable=GrassBurnable())


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

    @staticmethod
    def make(x, y):
        return make_water_entity(x, y)

    def get_entities(self):
        return [self.make(x, y) for x, y in self.coords]

    def get_random_pool_point(self, room):
        if room.terrain != Terrain.POOL:
            raise ValueError("Cannot create river in room with no pool tiles.")
        x, y = room.random_point()
        while not self.game_map.pool[x, y]:
            x, y = room.random_point()
        return x, y
