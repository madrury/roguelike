from tdl.map import Map
import numpy as np
from random import randint

from entity import Entity


class Rectangle:

    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    @property
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

class GameMap(Map):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.explored = np.zeros((width, height)).astype(bool)


def make_map(game_map, map_config, player):
    # Destructure the map_config dictionary into local variables.
    map_config_keys = [
        'width', 'height', 'room_min_size', 'room_max_size', 'max_rooms']
    map_width, map_height, room_min_size, room_max_size, max_rooms = [
        map_config[key] for key in map_config_keys]
    rooms = []
    for r in range(max_rooms):
        # Create a new random room and add it to the map.
        width = randint(room_min_size, room_max_size)
        height = randint(room_min_size, room_max_size)
        x = randint(0, map_width - width - 1)
        y = randint(0, map_height - height - 1)
        new_room = Rectangle(x, y, width, height)
        for other_room in rooms:
            if new_room.intersect(other_room):
                break
        else:
            create_room(game_map, new_room)
        num_rooms = len(rooms)
        # Place player in the center of the first room.
        if num_rooms == 0:
            player.x, player.y = new_room.center
        # Create a tunnel connecting the new room to the previous room.
        else:
            prev_room = rooms[num_rooms - 1] 
            add_tunnel(game_map, new_room, prev_room) 
        rooms.append(new_room)

def create_room(game_map, room):
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            make_transparent_and_walkable(game_map, x, y)

def make_transparent_and_walkable(game_map, x, y):
    game_map.walkable[x, y] = True
    game_map.transparent[x, y] = True

def add_tunnel(game_map, new_room, prev_room):
    cx, cy = new_room.center
    prev_x, prev_y = prev_room.center
    if randint(0, 1) == 1:
        create_h_tunnel(game_map, prev_x, cx, prev_y)
        create_v_tunnel(game_map, prev_y, cy, cx)
    else:
        create_v_tunnel(game_map, prev_y, cy, prev_x)
        create_h_tunnel(game_map, prev_x, cx, cy)

def create_h_tunnel(game_map, x1, x2, y):
    x1, x2 = min(x1, x2), max(x1, x2)
    for x in range(x1, x2 + 1):
        make_transparent_and_walkable(game_map, x, y)

def create_v_tunnel(game_map, y1, y2, x):
    y1, y2 = min(y1, y2), max(y1, y2)
    for y in range(y1, y2 + 1):
        make_transparent_and_walkable(game_map, x, y)
