import random
import numpy as np


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
            x_pin = random.randint(0, width - room.width)
            y_pin = random.randint(0, height - room.height)
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


def random_dungeon_room(width=18, 
                        height=18, 
                        max_rectangles=20,
                        max_rectangle_width=5,
                        max_rectangle_height=5,
                        n_rectangle_trys=500):
    """Generate a random dungeon room by placing random rectangles and
    building up a connected reigon.
    """
    room = DungeonRoom(width, height)
    for n in range(n_rectangle_trys):
        rect_width = random.randint(1, max_rectangle_width)
        rect_height = random.randint(1, max_rectangle_height)
        x = random.randint(0, width - rect_width)
        y = random.randint(0, height - rect_height)
        rect = Rectangle(x, y, rect_width, rect_height)
        if n == 0:
            room.add_rectangle(rect)
        elif room.intersect_rectangle(rect):
            room.add_rectangle(rect)
        if len(room.rectangles) >= max_rectangles:
            break
    return room


class PinnedDungeonRoom:
    """A DungeonRoom pinned onto a position in a larger map."""
    def __init__(self, room, position):
        self.x, self.y = position
        self.room = room

    def contains(self, point):
        point[0] - self.x, point[1] - self.x in self.room

    def __iter__(self):
        for x, y in self.room:
            yield self.x + x, self.y + y

    def intersect(self, other):
        for r1, r2 in zip(self.room.rectangles, other.room.rectangles):
            r2_in_r1_coord = Rectangle(other.x - self.x + r2.x1,
                                       other.y - self.x + r2.y1,
                                       r2.width,
                                       r2.height)
            if r1.intersect(r2_in_r1_coord):
                return True
        return False

    def random_point(self):
        room_point = self.room.random_point()
        return (self.x + room_point[0], self.y + room_point[1])


class DungeonRoom:
    """A single room in the dungeon.

    A DungeonRooom is made up of a collection of rectangles, and comes
    with its own local coordinate system.
    """
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.rectangles = []
        self.room = np.zeros((self.width, self.height)).astype(bool)

    def __iter__(self):
        for r in self.rectangles:
            for x, y in r:
                yield x, y

    def add_rectangle(self, rectangle):
        for point in rectangle:
            self.room[point[0], point[1]] = True
        self.rectangles.append(rectangle)

    def intersect(self, other):
        rectangle_pairs = zip(self.rectangles, other.rectangles)
        return any(r1.intersect(r2) for r1, r2 in rectangle_pairs)

    def intersect_rectangle(self, rectangle):
        return any(r.intersect(rectangle) for r in self.rectangles)

    def __contains__(self, point):
        return any(point in r for r in self.rectangles)

    def print_room(self):
        print(np.array(['.', '#'])[self.room.astype(int)])

    def random_rectangle(self):
        return random.choice(self.rectangles)

    def random_point(self):
        return self.random_rectangle().random_point()


class Rectangle:
    """A rectangle, DungeonRooms are composed of intersecting rectangles.

    Note: Rectangles do not contain thier right and lower boundaries.
    """
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.width = w
        self.height = h
        self.x2 = x + w
        self.y2 = y + h

    def __iter__(self):
        for i in range(self.x1, self.x2):
            for j in range(self.y1, self.y2):
                yield i, j

    def __contains__(self, point):
        return (self.x1 <= point[0] < self.x2 and
                self.y1 <= point[1] < self.y2)

    def random_point(self):
        return (random.randint(self.x1, self.x2 - 1),
                random.choice(self.y1, self.y2 - 1))

    @property
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        return (self.x1 < other.x2 and self.x2 > other.x1 and
                self.y1 < other.y2 and self.y2 > other.y1)
