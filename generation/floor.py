import random
import itertools
import numpy as np

from utils.utils import get_connected_components, fill_connected_components

from generation.floor_schedule import FloorType
from generation.special_rooms import ROOM_CONSTRUCTORS
from generation.room import PinnedMultiRectangularDungeonRoom, PinnedLayoutRoom
from generation.tunnel import random_tunnel_between_pinned_rooms


def make_floor(floor_config, floor_schedule):
    """Create a floor of the dungon given a configuration."""
    floor_width = floor_config['width']
    floor_height = floor_config['height']
    floor_type = floor_schedule['type']
    rooms = make_initial_rooms(floor_schedule['rooms'])
    if floor_type == FloorType.ROOMS_AND_TUNNELS:
        floor = RoomsAndTunnelsFloor.random(
            floor_width,
            floor_height,
            floor_schedule=floor_schedule,
            rooms=rooms,
            room_counter_init=len(rooms))
    elif floor_type == FloorType.CAVE:
        print(floor_width, floor_height)
        floor = CaveFloor.random(floor_width, floor_height)
            # TODO: Pass non-default generation parameters from the floor config.
            #floor_schedule=floor_schedule,
            #rooms=rooms)
    else:
        raise ValueError(f"Floor type {floor_type.name} not supported!")
    return floor


def make_initial_rooms(room_type_list):
    rooms = []
    for room_type in room_type_list:
        rooms.append(ROOM_CONSTRUCTORS[room_type].make())
    return rooms


class AbstractFloor:
    """Defines the interface for dungeon floor objects. These hold the
    metadata need for random generation of a dungeon floor layout; they hand
    off their information to the GameMap object during actual gameplay.

    Attributes
    ----------
    width: int
      The width of the dungeon floor.

    height: int
      The height of the dungeon floor.

    self.rooms: list of AbstractDungeonRoom objects.
      The rooms in the dungeon.

    self.objects: List[Entity]
      Static objects to populate the floor with.
    """
    def __init__(self, width=80, height=41):
        self.width = width
        self.height = height
        self.rooms = []
        self.objects = []

    @staticmethod
    def random():
        NotImplementedError

    def random_room(self):
        NotImplementedError

    def commit_to_game_map(self, game_map):
        NotImplementedError


class CaveFloor(AbstractFloor):

    def __init__(self, shape, *,
                 p=0.515,
                 destruct_num=3,
                 construct_num=5,
                 keep_passes=False):
        super().__init__(width=shape[0], height=shape[1])
        self.shape = shape
        self.p = p
        self.destruct_num = destruct_num
        self.construct_num = construct_num
        self._passes = []
        self.layout = None
        self.grow(keep_passes=keep_passes)
        print(self.layout)

    @staticmethod
    def random(width=80, height=41):
        floor = CaveFloor(shape=(width, height))
        floor.grow()
        return floor

    def random_room(self, shape=(10, 10)):
        # TODO: Actually implement this thing.
        return PinnedLayoutRoom(self.layout[15:26, 15:25], (15, 15))

    def commit_to_game_map(self, game_map):
        print(self.layout.shape, game_map.walkable.shape)
        coordinate_pairs = itertools.product(
            range(1, self.shape[0] - 1),
            range(1, self.shape[1] - 1))
        for x, y in coordinate_pairs:
            if self.layout[x, y]:
                game_map.make_transparent_and_walkable(x, y)
        for entity in self.objects:
            entity.commitable.commit(game_map)

    def grow(self, iterations=16, keep_passes=False):
        x = np.random.binomial(1, self.p, size=self.shape)
        for _ in range(iterations):
            if keep_passes:
                self._passes.append(x)
            x = self.single_pass(x)
        components = get_connected_components(x)
        x = fill_connected_components(x, components, n_to_keep=1)
        self.layout = x

    def single_pass(self, x):
        new = np.zeros(shape=self.shape, dtype=int)
        coordinate_pairs = itertools.product(
            range(1, self.shape[0] - 1),
            range(1, self.shape[1] - 1))
        for xidx, yidx in coordinate_pairs:
            center = x[xidx, yidx]
            view = x[(xidx-1):(xidx+2), (yidx-1):(yidx+2)]
            n_boundaries_filled = np.sum(view) - center
            if (center == 1) and n_boundaries_filled <= self.destruct_num:
                new[xidx, yidx] = 0
            elif (center == 0) and n_boundaries_filled >= self.construct_num:
                new[xidx, yidx] = 1
            else:
                new[xidx, yidx] = center
        return new


class RoomsAndTunnelsFloor(AbstractFloor):
    """A Floor of a dungeon.

    A floor of a dungeon is made up of a collection of dungeon features.  At
    the most basic level, PinnedDungeonRooms and Tunnels define the walkable
    space.  Additional terrain features (Pools, ...) are also stored.

    Additional Attributes
    ---------------------
    self.tunnels: list of Tunnel objects
      The tunnels in the dungeon.
    """
    def __init__(self, width=80, height=41):
        super().__init__(width=width, height=height)
        self.tunnels = []

    @staticmethod
    def random(width=80,
               height=41,
               n_rooms_to_try=50,
               n_room_placement_trys=25,
               floor_schedule=None,
               floor=None,
               room_counter_init=0,
               rooms=None):
        """Generate a random dungeon floor in the rooms and tunnels style with
        given parameters.

        make_floor is the intended public interface for this function.

        Parameters
        ----------
        width: int
          The width of the dungeon floor.

        height: int
          The height of the dungeon floor.

        n_rooms_to_try: int
          The maximum number of rooms to generate and attempt to place.

        n_room_placement_trys: int
          The maximum number of times to attempt to place a single room.

        floor_schedule: dict
          Configuration for random generation of a single room.

        floor: DungeonFloor
          An optional DungeonFloor object.  If passed, the random rooms will be
          added to this floor.

        room_counter_init: int
          Number to initialzie the room counter to.  Used in case the process is
          seeded with some rooms already created.

        rooms: List[PinnedRoom]
          Pre-created rooms to be added to the floor.

        Returns
        -------
        floor: DungeonFloor object
          The generated dungeon floor.
        """
        if floor_schedule == None:
            floor_schedule = {}
        if floor == None:
            floor = RoomsAndTunnelsFloor(width, height)
        for room in rooms:
            floor.add_pinned_room(room)
        for n in range(room_counter_init, n_rooms_to_try):
            room = PinnedMultiRectangularDungeonRoom.random(**floor_schedule)
            for _ in range(n_room_placement_trys):
                x_pin = random.randint(1, width - room.width - 1)
                y_pin = random.randint(1, height - room.height - 1)
                pinned_room = PinnedMultiRectangularDungeonRoom(room, (x_pin, y_pin))
                if n == 0:
                    floor.add_pinned_room(pinned_room)
                    break
                elif not any(pinned_room.intersect(pr) for pr in floor.rooms):
                    floor.add_pinned_room(pinned_room)
                    break
            if len(floor.rooms) >= floor_schedule['max_rooms']:
                break
        # Add tunnels between the consecutive rooms.
        for r1, r2 in zip(floor.rooms[:-1], floor.rooms[1:]):
            t1, t2 = random_tunnel_between_pinned_rooms(r1, r2)
            floor.add_tunnel(t1)
            floor.add_tunnel(t2)
        # Add a pool.
        return floor

    def random_room(self):
        return random.choice(self.rooms)

    def commit_to_game_map(self, game_map):
        for room in self.rooms:
            for x, y in room:
                game_map.make_transparent_and_walkable(x, y)
        for tunnel in self.tunnels:
            for x, y in tunnel:
                game_map.make_transparent_and_walkable(x, y)
        for entity in self.objects:
            entity.commitable.commit(game_map)

    def add_pinned_room(self, pinned_room):
        self.rooms.append(pinned_room)
        if pinned_room.objects:
            self.objects.extend(pinned_room.objects)

    def add_tunnel(self, tunnel):
        self.tunnels.append(tunnel)