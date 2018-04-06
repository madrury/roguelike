import random
import numpy as np

from .room import PinnedDungeonRoom, random_dungeon_room

def random_dungeon_floor(width=80, 
                         height=43, 
                         max_rooms=25,
                         n_rooms_to_try=50,
                         n_room_placement_trys=25,
                         room_config=None):
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
    return floor


class DungeonFloor:
    """A Floor of a dungeon.

    A floor of a dungeon is made up of multiple PinnedDungeonRooms.
    """
    def __init__(self, width=80, height=43):
        self.width = width
        self.height = height
        self.rooms = []
        self.tunnels = []
        self.floor = np.zeros((width, height)).astype(bool)

    def add_pinned_room(self, pinned_room):
        for x, y in pinned_room:
            self.floor[x, y] = True
        self.rooms.append(pinned_room)

    def print_floor(self):
        arr = np.array(['.', '#'])[self.floor.astype(int)].T
        for row in arr:
            print(''.join(row))

