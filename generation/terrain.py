import random
import numpy as np

from colors import random_light_green, random_light_water, random_dark_water
from entity import Entity

from etc.enum import Terrain, EntityTypes, RenderOrder
from etc.colors import COLORS
from utils.utils import adjacent_coordinates, random_adjacent
from game_objects.terrain import (
    UpwardStairs, DownwardStairs, Door, StationaryTorch, Water, Ice, Grass,
    Shrub)
from components.shimmer import WaterShimmer
from components.burnable import GrassBurnable, WaterBurnable


def add_random_terrain(game_map, terrain_config):
    """Generate random terrain in a game map, according to a terrain
    configuration dictionary.

    Parameters
    ----------
    game_map: Map object.
      The current game map.  Assumed to be empty of terrain.

    terrain_config: dict
      Dictionary containing configuration parameters governing how to grow
      terrain for this floor of the dungeon.

    Returns:
      None

    This method does not return a meaningful value, it instead modified
    game_map by populating it with terrain.
    """
    terrain = []
    # Grow pools of water.
    terrain.extend(
        grow_random_single_terrain(
            game_map, Pool.grow_in_random_room,
            min_terrains=terrain_config['min_pools'],
            max_terrains=terrain_config['max_pools'],
            terrain_proportion=terrain_config['pool_room_proportion']))
    # Grow rivers.
    min_rivers, max_rivers = (
        terrain_config['min_rivers'], terrain_config['max_rivers'])
    n_rivers = random.randint(min_rivers, max_rivers)
    for _ in range(n_rivers):
        river = random_river(game_map)
        terrain.extend(river.get_entities(game_map))
    # Grow patches of grass.
    terrain.extend(
        grow_random_single_terrain(
            game_map, PatchOfGrass.grow_in_random_room,
            min_terrains=terrain_config['min_grass'],
            max_terrains=terrain_config['max_grass'],
            terrain_proportion=terrain_config['grass_room_proportion']))
    # Grow patches of shrubs.
    terrain.extend(
        grow_random_single_terrain(
            game_map, PatchOfShrubs.grow_in_random_room,
            min_terrains=terrain_config['min_shrubs'],
            max_terrains=terrain_config['max_shrubs'],
            terrain_proportion=terrain_config['shrubs_room_proportion']))
    # Grow patches of ice.
    terrain.extend(
        grow_random_single_terrain(
            game_map, PatchOfIce.grow_in_random_room,
            min_terrains=terrain_config['min_ice'],
            max_terrains=terrain_config['max_ice'],
            terrain_proportion=terrain_config['ice_room_proportion']))
    # Place the upward and downward stairs
    if terrain_config.get('upward_stairs', True):
        stair_placer = UpwardsStairsPlaceable()
        terrain.append(stair_placer.place_one(game_map))
    if terrain_config.get('downward_stairs', True):
        stair_placer = DownwardsStairsPlaceable()
        terrain.append(stair_placer.place_one(game_map))
    # Place any torches
    torch_placer = TorchPlaceable()
    terrain.extend(
        torch_placer.place_many(
            game_map,
            min_objects=terrain_config['min_torches'],
            max_objects=terrain_config['max_torches']))
    # Place any doors
    door_placer = DoorPlaceable()
    terrain.extend(
        door_placer.place_many(game_map, min_objects=4, max_objects=6))
    # We've been using this array to track when terrain was generated in a tile
    # through the terrain generation process.  Now we want to commit them to
    # the map, but the array will block terrain from being places anywhere that
    # it contains a true.  We just want to force commit all the terrain we
    # generated, so we zero out the array first.
    game_map.terrain[:, :] = False
    game_map.water[:, :] = False
    for t in terrain:
        t.commitable.commit(game_map)

def grow_random_single_terrain(game_map, terrain_creator, *,
                               min_terrains, max_terrains, terrain_proportion):
    """Grow a single type of terrain in a game map according to some
    configuration parameters.
    """
    n_terrains = random.randint(min_terrains, max_terrains)
    terrain = []
    for _ in range(n_terrains):
        t = terrain_creator(game_map, proportion=terrain_proportion)
        terrain.extend(t.get_entities(game_map))
    return terrain

def grow_in_random_room(terrain, game_map, *, stay_in_room, proportion):
    """Pick a random room of the game map and grow some terrain there."""
    pinned_room = random.choice(game_map.floor.rooms)
    while pinned_room.terrain != None:
        pinned_room = random.choice(game_map.floor.rooms)
    t = terrain(game_map, pinned_room)
    t.seed()
    t.grow(stay_in_room=stay_in_room, proportion=proportion)
    return t


#-----------------------------------------------------------------------------
# Placeable Terrain
#-----------------------------------------------------------------------------
class Placeable:
    """Base class for terrain that is placed.

    Terrain is placed by finding squares of the map whose local neighbourhood
    matches a set of supplied masks.  For example, we may want to place stairs
    in a straight segment of wall, or a treasure chest in a corner.
    """
    def place_one(self, game_map):
        obj = None
        while not obj:
            x = random.randint(0, game_map.width - 1)
            y = random.randint(0, game_map.height - 1)
            if self.is_placable(game_map, x, y):
                return self.make(game_map, x, y)

    def place_many(self, game_map, min_objects, max_objects):
        objects = []
        n_objects = random.randint(min_objects, max_objects)
        while len(objects) != n_objects:
            obj = self.place_one(game_map)
            if obj:
                objects.append(obj)
        return objects

    def is_placable(self, game_map, x, y):
        local_map = game_map.walkable[(x-1):(x+2), (y-1):(y+2)]
        return (game_map.within_bounds(x, y, buffer=1)
                and not game_map.terrain[x, y]
                and any((local_map == mask).all() for mask in self.masks))

    def make(self, game_map, x, y):
        raise NotImplementedError("Subclasses of Placeable need to implement make.")


#-----------------------------------------------------------------------------
# Stationary Torches
#-----------------------------------------------------------------------------
class TorchPlaceable(Placeable):
    """Torches are placed:

        - In straight segments of walls.
        - nestled into corners.
        - In three by three open squares in the middle of rooms.
    """
    masks = [
        np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]]),
        np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]]),
        np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]]),
        np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]]),
        np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]]),
        np.array([[1, 1, 0], [1, 1, 0], [0, 0, 0]]),
        np.array([[0, 0, 0], [1, 1, 0], [1, 1, 0]]),
        np.array([[0, 1, 1], [0, 1, 1], [0, 0, 0]]),
        np.array([[0, 0, 0], [0, 1, 1], [0, 1, 1]])
    ]

    def make(self, game_map, x, y):
        game_map.terrain[x, y] = True
        return StationaryTorch.make(game_map, x, y)


#-----------------------------------------------------------------------------
# Stairs
#-----------------------------------------------------------------------------
class StairsPlacable(Placeable):
    """Stairs are placed nestled into straight segments of walls, or into
    corners.
    """
    masks = [
        np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]]),
        np.array([[1, 1, 1], [0, 0, 0], [0, 0, 0]]),
        np.array([[1, 0, 0], [1, 0, 0], [1, 0, 0]]),
        np.array([[1, 1, 0], [1, 1, 0], [0, 0, 0]]),
        np.array([[0, 0, 0], [1, 1, 0], [1, 1, 0]]),
        np.array([[0, 1, 1], [0, 1, 1], [0, 0, 0]]),
        np.array([[0, 0, 0], [0, 1, 1], [0, 1, 1]])
    ]

class UpwardsStairsPlaceable(StairsPlacable):

    def make(self, game_map, x, y):
        game_map.terrain[x, y] = True
        return UpwardStairs.make(game_map, x, y)

class DownwardsStairsPlaceable(StairsPlacable):

    def make(self, game_map, x, y):
        game_map.terrain[x, y] = True
        return DownwardStairs.make(game_map, x, y)


#-----------------------------------------------------------------------------
# Doors
#-----------------------------------------------------------------------------
class DoorPlaceable(Placeable):
    """Doors are placed in narrow hallways.  They can be freely moved through,
    but block visibility, and will block the movement of some stupider
    monsters.
    """
    masks = [
        np.array([[0, 1, 0], [0, 1, 0], [0, 1, 0]]),
        np.array([[0, 0, 0], [1, 1, 1], [0, 0, 0]]),
    ]

    def make(self, game_map, x, y):
        return Door.make(game_map, x, y)

#-----------------------------------------------------------------------------
# Growable Terrain
#-----------------------------------------------------------------------------
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

    def seed(self):
        x, y = self.room.random_point()
        while self.game_map.terrain[x, y]:
            x, y = self.room.random_point()
        self.coords.append((x, y))

    def grow(self, stay_in_room=False, proportion=None, n_attempts=None):
        """Grow the terrain using the algorithm described in the class
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
        """Create a list of entities representing the grown terrain."""
        return [self.make(game_map, x, y) for x, y in self.coords]


class Pool(Growable):
    """A pool of water in a room.

    Pools are made of water entities.  Most monsters will avoid pools of water,
    and passing through water drains the player's swim stamina.
    """
    def __init__(self, game_map, room):
        super().__init__(game_map, room)
        room.terrain = Terrain.POOL

    @staticmethod
    # Rename to make_one_tile
    def make(game_map, x, y):
        game_map.water[x, y] = True
        return Water.make(game_map, x, y)

    @staticmethod
    def grow_in_random_room(game_map, proportion):
        return grow_in_random_room(Pool, game_map,
                                   stay_in_room=False,
                                   proportion=proportion)


class PatchOfIce(Growable):
    """A patch of ice in a room.

    Ice is travesable, but entities will slip on the ice, which essentailly
    doubles their movement speed in any direction.
    """
    def __init__(self, game_map, room):
        super().__init__(game_map, room)
        room.terrain = Terrain.ICE_PATCH

    @staticmethod
    def make(game_map, x, y):
        return Ice.make(game_map, x, y)

    @staticmethod
    def grow_in_random_room(game_map, proportion):
        return grow_in_random_room(PatchOfIce, game_map,
                                   stay_in_room=True,
                                   proportion=proportion)


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

    @staticmethod
    def grow_in_random_room(game_map, proportion):
        return grow_in_random_room(PatchOfGrass, game_map,
                                   stay_in_room=True,
                                   proportion=proportion)


class PatchOfShrubs(Growable):
    """A dense patch of shrubs.

    Shrubs block visibility, but not movement.  They turn into grass when
    trampled, and can be burned.
    """
    def __init__(self, game_map, room):
        super().__init__(game_map, room)
        room.terrain = Terrain.SHRUBS

    @staticmethod
    def make(game_map, x, y):
        return Shrub.make(game_map, x, y)

    @staticmethod
    def grow_in_random_room(game_map, proportion):
        return grow_in_random_room(PatchOfShrubs, game_map,
                                   stay_in_room=True,
                                   proportion=proportion)

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
