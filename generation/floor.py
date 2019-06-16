import random
import numpy as np

from generation.floor_schedule import FloorType
from generation.room import PinnedDungeonRoom, random_dungeon_room
from generation.special_rooms import ROOM_CONSTRUCTORS
from generation.tunnel import random_tunnel_between_pinned_rooms


def make_floor(floor_config, floor_schedule):
    """Create a floor of the dungon given a configuration."""
    floor_width = floor_config['width']
    floor_height = floor_config['height']
    floor_type = floor_schedule['type']
    if floor_type == FloorType.STANDARD:
        rooms = make_initial_rooms(floor_schedule['rooms'])
        floor = random_rooms_and_tunnels_floor(
            floor_width,
            floor_height,
            floor_schedule=floor_schedule,
            rooms=rooms,
            room_counter_init=len(rooms))
    else:
        raise ValueError(f"Floor type {floor_type.name} not supported!")
    return floor


def make_initial_rooms(room_type_list):
    rooms = []
    for room_type in room_type_list:
        rooms.append(ROOM_CONSTRUCTORS[room_type].make())
    return rooms


def random_rooms_and_tunnels_floor(width=80,
                         height=41,
                         n_rooms_to_try=50,
                         n_room_placement_trys=25,
                         floor_schedule=None,
                         floor=None,
                         room_counter_init=0,
                         rooms=None):
    """Generate a random dungeon floor with given parameters.

    make_floor is the intended interface for this function.

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
        room = random_dungeon_room(**floor_schedule)
        for _ in range(n_room_placement_trys):
            x_pin = random.randint(1, width - room.width - 1)
            y_pin = random.randint(1, height - room.height - 1)
            pinned_room = PinnedDungeonRoom(room, (x_pin, y_pin))
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


class RoomsAndTunnelsFloor:
    """A Floor of a dungeon.

    A floor of a dungeon is made up of a collection of dungeon features.  At
    the most basic level, PinnedDungeonRooms and Tunnels define the walkable
    space.  Additional terrain features (Pools, ...) are also stored.

    Parameters
    ----------
    width: int
      The width of the dungeon floor.

    height: int
      The height of the dungeon floor.

    Attributes
    ----------
    self.rooms: list of PinnedDungeonRoom objects.
      The rooms in the dungeon.

    self.tunnels: list of Tunnel objects
      The tunnels in the dungeon.

    self.objects: List[Entity]
      Static objects to populate the floor with.

    self.floor: np.array of bool
      Array of transparant tiles.  Only used for printing.
    """
    def __init__(self, width=80, height=41):
        self.width = width
        self.height = height
        self.rooms = []
        self.tunnels = []
        self.objects = []
        self.floor = np.zeros((width, height)).astype(bool)

    def add_pinned_room(self, pinned_room):
        for x, y in pinned_room:
            self.floor[x, y] = True
        self.rooms.append(pinned_room)
        if pinned_room.objects:
            self.objects.extend(pinned_room.objects)

    def add_tunnel(self, tunnel):
        for x, y in tunnel:
            self.floor[x, y] = True
        self.tunnels.append(tunnel)

    def print_floor(self):
        arr = np.array(['.', '#'])[self.floor.astype(int)].T
        for row in arr:
            print(''.join(row))