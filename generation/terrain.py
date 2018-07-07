import random

from colors import random_light_green, random_light_water, random_dark_water
from entity import Entity

from etc.enum import Terrain, EntityTypes, RenderOrder
from etc.colors import COLORS
from utils.utils import adjacent_coordinates, random_adjacent
from game_objects.terrain import Water, Grass, Shrub
from components.shimmer import WaterShimmer
from components.burnable import GrassBurnable, WaterBurnable


def add_random_terrain(game_map, terrain_config):
    floor = game_map.floor

    terrain = []
    terrain.extend(
        random_growable(game_map, random_pool,
                        min_terrains=terrain_config['min_pools'],
                        max_terrains=terrain_config['max_pools'],
                        terrain_proportion=terrain_config['pool_room_proportion']))

    min_rivers, max_rivers = (
        terrain_config['min_rivers'], terrain_config['max_rivers'])
    n_rivers = random.randint(min_rivers, max_rivers)
    for _ in range(n_rivers):
        river = random_river(game_map)
        terrain.extend(river.get_entities(game_map))

    terrain.extend(
        random_growable(game_map, random_grass,
                        min_terrains=terrain_config['min_grass'],
                        max_terrains=terrain_config['max_grass'],
                        terrain_proportion=terrain_config['grass_room_proportion']))
    terrain.extend(
        random_growable(game_map, random_shrubs,
                        min_terrains=terrain_config['min_shrubs'],
                        max_terrains=terrain_config['max_shrubs'],
                        terrain_proportion=terrain_config['shrubs_room_proportion']))
    # We've been using this array to track when terrain was generated in a tile
    # through the terrain generation process.  Now we want to commit them to
    # the map, but the array will block terrain from being places anywhere that
    # it contains a true.  We just want to force commit all the terrain we
    # generated, so we zero out the array first.
    game_map.terrain[:, :] = False
    game_map.water[:, :] = False
    for t in terrain:
        t.commitable.commit(game_map)


def random_growable(game_map, terrain_creator, *,
                        min_terrains, max_terrains, terrain_proportion):
    n_terrains = random.randint(min_terrains, max_terrains)
    terrain = []
    for _ in range(n_terrains):
        t = terrain_creator(game_map, proportion=terrain_proportion)
        terrain.extend(t.get_entities(game_map))
    return terrain


class Growable:
    """Base class for terrain that can be grown.

    Terrain is grown by first seeding a random point in a rooma and placing
    terrain there. Then we repeatadely expand this seed by choosing a point
    adjaent to an already grown terrain, and placing a terrain there if
    possible. 

    Parameters
    ----------
    game_map: GameMap object
      The game map.

    room: PinnedDungeonRoom object
      The room to grow the terrain in.

    Attributes
    ----------
    coords: List[(int, int)]
      A list of the currently grown coordinates.
    """
    def __init__(self, game_map, room):
        self.game_map = game_map
        self.room = room
        self.coords = [] 

    def __iter__(self):
        yield from iter(self.coords)

    def seed(self):
        x, y = self.room.random_point()
        while self.game_map.terrain[x, y]:
            x, y = self.room.random_point()
        self.coords.append((x, y))

    def grow(self, stay_in_room=False, proportion=None, n_attempts=None):
        """Grow the room using the algorithm described in the class
        docstring.
        
        Parameters
        ----------
        stay_in_room: bool
          Should the terrain stay within the bounds of the room it is grown in?
          If False, any space terrain is spawned in will be made walkable.

        n_attempts: int
          The number of times to attempt to spawn a new piece of terrain.

        proportion: float
          A scaling factor for how much terrain to grow.  Used if n_atempts is
          not passed.
        """
        if not n_attempts:
            n_attempts = int(
                proportion * self.room.width * self.room.height)
        self.seed()
        for i in range(n_attempts):
            coord = random.choice(self.coords)
            x, y = random_adjacent(coord)
            is_valid = not stay_in_room or self.game_map.walkable[x, y]
            already_occupied = self.game_map.terrain[x, y]             
            within_bounds = self.game_map.within_bounds(x, y, buffer=1)
            if is_valid and not already_occupied and within_bounds:
                self.game_map.terrain[x, y] = True
                self.coords.append((x, y))

    def get_entities(self, game_map):
        return [self.make(game_map, x, y) for x, y in self]


#-----------------------------------------------------------------------------
# Pool
#-----------------------------------------------------------------------------
class Pool(Growable):
    """A pool of water in a room."""
    def __init__(self, game_map, room):
        super().__init__(game_map, room)
        room.terrain = Terrain.POOL

    @staticmethod
    def make(game_map, x, y):
        game_map.water[x, y] = True
        return Water.make(game_map, x, y)


def random_pool(game_map, proportion):
    """Grow a pool of water in a random room on a map."""
    pinned_room = random.choice(game_map.floor.rooms)
    while pinned_room.terrain != None:
        pinned_room = random.choice(game_map.floor.rooms)
    pool = Pool(game_map, pinned_room)
    pool.seed()
    pool.grow(stay_in_room=False,
              proportion=proportion)
    return pool


#-----------------------------------------------------------------------------
# River
#-----------------------------------------------------------------------------
class River:
    """A river connecting two pools of water.

    Parameters
    ----------
    game_map: GameMap object
    
    source_room: PinnedDungeonRoom object
      The room contining the pool to use a source of the river.

    dest_room: PinnedDungeonRoom object
      The room containing the pool to use as a destination of the river.

    width: int
      The width of the river.
    """
    def __init__(self, game_map, source_room, dest_room, width=1):
        self.game_map = game_map
        self.source_point = self.get_random_pool_point(source_room)
        self.dest_point = self.get_random_pool_point(dest_room)
        self.coords = set()
        self.grow()
        self.thicken(width)

    def grow(self):
        """Choose a random point in both the source and destination pool, and
        fill the path between them with water terain.
        """
        x0, y0 = self.source_point
        x1, y1 = self.dest_point
        path = self.game_map.compute_path(x0, y0, x1, y1)
        for x, y in path:
            self.game_map.terrain[x, y] = True
            self.coords.add((x, y))

    def thicken(self, width=1):
        for _ in range(width - 1):
            for river_coord in self.coords:
                for coord in adjacent_coordinates(river_coord):
                    x, y = coord
                    if not self.game_map.terrain[x, y]:
                        self.game_map.terrain[x, y] = True
                        new_coords.add(coord)
            self.coords.update(new_coords)

    @staticmethod
    def make(game_map, x, y):
        game_map.water[x, y] = True
        return Water.make(game_map, x, y)

    def get_entities(self, game_map):
        return [self.make(game_map, x, y) for x, y in self.coords]

    def get_random_pool_point(self, room):
        if room.terrain != Terrain.POOL:
            raise ValueError("Cannot create river in room with no pool tiles.")
        x, y = room.random_point()
        while not self.game_map.water[x, y]:
            x, y = room.random_point()
        return x, y


def random_river(game_map):
    """Grow a river between two pools of water."""
    r1 = random.choice(game_map.floor.rooms)
    while r1.terrain != Terrain.POOL:
        r1 = random.choice(game_map.floor.rooms)
    r2 = random.choice(game_map.floor.rooms)
    while r1 == r2 or r2.terrain != Terrain.POOL:
        r2 = random.choice(game_map.floor.rooms)
    river = River(game_map, r1, r2)
    return river


#-----------------------------------------------------------------------------
# Grass
#-----------------------------------------------------------------------------
class PatchOfGrass(Growable):
    """A grassy room.

    Grass is burnable, so fire spells used in the grassy room will spread.
    """
    def __init__(self, game_map, room):
        super().__init__(game_map, room)
        room.terrain = Terrain.GRASS

    @staticmethod
    def make(game_map, x, y):
        return Grass.make(game_map, x, y)
        
def random_grass(game_map, proportion):
    """Grow grass in a random room on the game map."""
    pinned_room = random.choice(game_map.floor.rooms)
    while pinned_room.terrain != None:
        pinned_room = random.choice(game_map.floor.rooms)
    grass = PatchOfGrass(game_map, pinned_room)
    grass.grow(stay_in_room=True, proportion=proportion)
    return grass


#-----------------------------------------------------------------------------
# Field of Shrubs
#-----------------------------------------------------------------------------
class PatchOfShrubs(Growable):

    def __init__(self, game_map, room):
        super().__init__(game_map, room)
        room.terrain = Terrain.SHRUBS

    @staticmethod
    def make(game_map, x, y):
        return Shrub.make(game_map, x, y)

def random_shrubs(game_map, proportion):
    """Grow grass in a random room on the game map."""
    pinned_room = random.choice(game_map.floor.rooms)
    while pinned_room.terrain != None:
        pinned_room = random.choice(game_map.floor.rooms)
    shrubs = PatchOfShrubs(game_map, pinned_room)
    shrubs.grow(stay_in_room=True, proportion=proportion)
    return shrubs
