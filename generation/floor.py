import random
import numpy as np

from generation.room import PinnedDungeonRoom, random_dungeon_room
from generation.tunnel import random_tunnel_between_pinned_rooms


def make_floor(floor_config, room_config):
    """Generate a random dungeon floor with given parameters."""
    floor_config_keys = ['width', 'height', 'max_rooms']
    floor_width, floor_height, max_rooms = [
        floor_config[key] for key in floor_config_keys]
    floor = random_dungeon_floor(floor_width, floor_height, 
                                 max_rooms=max_rooms,
                                 room_config=room_config)
    return floor

def random_dungeon_floor(width=80, 
                         height=43, 
                         max_rooms=25,
                         n_rooms_to_try=50,
                         n_room_placement_trys=25,
                         room_config=None):
    """Generate a random dungeon floor with given parameters.

    make_floor is the intended interface for this function.

    Parameters
    ----------
    width: int
      The width of the dungeon floor.

    height: int
      The height of the dungeon floor.

    max_rooms: int
      The maximum number of rooms in the floor.

    min_pools: int
      The minumum number of water pools in the floor.

    max_pools: int
      The maximum number of water pools in the floor.

    n_rooms_to_try: int
      The maximum number of rooms to generate and attempt to place.

    n_room_placement_trys: int
      The maximum number of times to attempt to place a single room.

    room_config: dict
      Configuration for random generation of a single room.

    Returns
    -------
    floor: DungeonFloor object
      The generated dungeon floor.
    """
    if room_config == None:
        room_config = {}
    floor = DungeonFloor(width, height)
    for n in range(n_rooms_to_try):
        room = random_dungeon_room(**room_config)
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
        if len(floor.rooms) >= max_rooms:
            break
    # Add tunnels between the consecutive rooms.
    for r1, r2 in zip(floor.rooms[:-1], floor.rooms[1:]):
        t1, t2 = random_tunnel_between_pinned_rooms(r1, r2)
        floor.add_tunnel(t1)
        floor.add_tunnel(t2)
    # Add a pool.
    return floor


class DungeonFloor:
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

    self.Pool: list of Pool objects.
      Pools of water in the dungeon.

    self.floor: np.array of bool
      Array of transparant tiles.  Only used for printing. 
    """
    def __init__(self, width=80, height=43):
        self.width = width
        self.height = height
        self.rooms = []
        self.tunnels = []
        self.pools = []
        self.floor = np.zeros((width, height)).astype(bool)

    def add_pinned_room(self, pinned_room):
        for x, y in pinned_room:
            self.floor[x, y] = True
        self.rooms.append(pinned_room)

    def add_tunnel(self, tunnel):
        for x, y in tunnel:
            self.floor[x, y] = True
        self.tunnels.append(tunnel)

    def add_pool(self, pool):
        self.pools.append(pool)

    def print_floor(self):
        arr = np.array(['.', '#'])[self.floor.astype(int)].T
        for row in arr:
            print(''.join(row))