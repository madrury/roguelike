import random
import numpy as np


class AbstractDungeonRoom:
    """Defines the interface for dungeon room objects. Each floor must
    contain some number of rooms to assist in monster, item, and terain
    generating code.

    Attributes
    ----------
    terrain: Terrain enum entry.
      Tracks if terrain has been added to this room. Used when procedurally
      generating terrain for the floor.

    monsters: bool
      Tracks if monsters have been spawned in the room. Used when
      procedurally generating monsters populating the floor.

    objects:
      Objects occupying this room that should be added to the parent floor.
      These are added to the map when the floor is finally commited.
    """
    def __init__(self, width, height, *,
                 terrain=None,
                 monsters=None,
                 objects=None):
        self.width = width
        self.height = height
        self.monsters = monsters
        self.objects = objects
        self.terrain = terrain

    def random_point(self):
        raise NotImplementedError


class PinnedLayoutRoom(AbstractDungeonRoom):

    def __init__(self, layout, position, *,
                 terrain=None,
                 monsters=None,
                 objects=None):
        super().__init__(
            layout.shape[0], layout.shape[1],
            terrain=terrain,
            monsters=monsters,
            objects=objects)
        self.x, self.y = position
        self.layout = layout.copy()

    def random_point(self):
        shape = self.layout.shape
        point = None
        while point == None:
            x, y = random.randint(0, shape[0] - 1), random.randint(0, shape[1] - 1)
            if self.layout[x, y]:
                point = (x, y)
        return (self.x + x, self.y + y)


class PinnedMultiRectangularDungeonRoom(AbstractDungeonRoom):
    """A DungeonRoom pinned onto a position in a larger map.

    A room comes with a coordinate system local to that room, as explained
    below.  Objects of this class are rooms that are pinned onto a larger
    coordinate system, usualy a dungeon floor.

      A Dungeon Floor.
    +-----------------------------------------------+
    |                                               |
    |    |The local coordinates are pinned on here. |
    |    |                                          |
    |    V A Room's Coordinate System.              |
    |    +----------------------+                   |
    |    |                      |                   |
    |    |   ####               |                   |
    |    |   ##########         |                   |
    |    |   #### #####         |                   |
    |    |        #####         |                   |
    |    +----------------------+                   |
    |                                               |
    |                                               |
    |                                               |
    +-----------------------------------------------+

    Attributes
    ----------
    x, y: ints
      The poisting the room is pinned in the enclosing coordinate system.

    room: MultiRectangularDungeonRoom
      The underlying room object.
    """
    def __init__(self, room, position, *,
                 terrain=None,
                 monsters=None,
                 objects=None):
        super().__init__(
            width=room.width, height=room.height,
            terrain=terrain,
            monsters=monsters,
            objects=objects)
        self.x, self.y = position
        self.room = room
        self.width, self.height = room.width, room.height

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
        return self.absolute_coordinates(room_point)

    def absolute_coordinates(self, point):
        return (self.x + point[0], self.y + point[1])

    @staticmethod
    def random(width=18,
               height=18,
               max_rectangles=20,
               max_rectangle_width=5,
               max_rectangle_height=5,
               n_rectangle_trys=500,
               **kwargs):
        """Generate a random dungeon room by placing random rectangles and
        building up a connected reigon.
        """
        room = MultiRectangularDungeonRoom(width, height)
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


class MultiRectangularDungeonRoom:
    """A single room in the dungeon.

    A DungeonRooom is made up of a collection of rectangles, and comes
    with its own local coordinate system.

    Example
    -------
    In [1]: r = DungeonRoom(15, 15)

    In [2]: r.add_rectangle(Rectangle(2, 2, 6, 6))

    In [3]: r.add_rectangle(Rectangle(6, 6, 6, 6))

    In [4]: r.print_room()
      v Coordinates (0, 0)
    ['.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.']
    ['.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.']
    ['.' '.' '#' '#' '#' '#' '#' '#' '.' '.' '.' '.' '.' '.' '.']
    ['.' '.' '#' '#' '#' '#' '#' '#' '.' '.' '.' '.' '.' '.' '.']
    ['.' '.' '#' '#' '#' '#' '#' '#' '.' '.' '.' '.' '.' '.' '.']
    ['.' '.' '#' '#' '#' '#' '#' '#' '.' '.' '.' '.' '.' '.' '.']
    ['.' '.' '#' '#' '#' '#' '#' '#' '#' '#' '#' '#' '.' '.' '.']
    ['.' '.' '#' '#' '#' '#' '#' '#' '#' '#' '#' '#' '.' '.' '.']
    ['.' '.' '.' '.' '.' '.' '#' '#' '#' '#' '#' '#' '.' '.' '.']
    ['.' '.' '.' '.' '.' '.' '#' '#' '#' '#' '#' '#' '.' '.' '.']
    ['.' '.' '.' '.' '.' '.' '#' '#' '#' '#' '#' '#' '.' '.' '.']
    ['.' '.' '.' '.' '.' '.' '#' '#' '#' '#' '#' '#' '.' '.' '.']
    ['.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.']
    ['.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.']
    ['.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.' '.']


    Attributes
    ----------
    height: int
      The height of the coordinate system containing the room.

    width: int
      The width of the coordinate system containing the room.

    rectangles: list of Rectangles
      The rectangles composing the room.

    room: np.array of bools
      A mask defining the room.  An entry is True if a point is in the room,
      False otherwise.
    """
    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.rectangles = []
        self.room = np.zeros((self.width, self.height)).astype(bool)

    def __iter__(self):
        """Iterate through all the points in a room.

        Each point is yielded by the iterator exactly one time.
        """
        seen = set()
        for r in self.rectangles:
            for x, y in r:
                if (x, y) not in seen and self.room[x, y]:
                    seen.add((x, y))
                    yield x, y

    def add_rectangle(self, rectangle):
        """Add a rectangle to a room."""
        for point in rectangle:
            self.room[point[0], point[1]] = True
        self.rectangles.append(rectangle)

    def intersect(self, other):
        """Do two rooms intersect?

        Rooms intersect when at least one rectangle from the first room
        intersects with a rectangle from the second room.
        """
        rectangle_pairs = zip(self.rectangles, other.rectangles)
        return any(r1.intersect(r2) for r1, r2 in rectangle_pairs)

    def intersect_rectangle(self, rectangle):
        """Does a room intersect a rectangle."""
        return any(r.intersect(rectangle) for r in self.rectangles)

    def __contains__(self, point):
        """Is a point in a room."""
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
        """Iterate through the points contained in a rectangle."""
        for i in range(self.x1, self.x2):
            for j in range(self.y1, self.y2):
                yield i, j

    def __contains__(self, point):
        """Is a point inside a rectangle."""
        return (self.x1 <= point[0] < self.x2 and
                self.y1 <= point[1] < self.y2)

    def random_point(self):
        """Draw a random point uniformly from a rectangle."""
        return (random.randint(self.x1, self.x2 - 1),
                random.randint(self.y1, self.y2 - 1))

    @property
    def center(self):
        """The center of a rectangle.

        When a dimesnsion of the rectangle is odd, the center is rounded down
        to the nearest integer.
        """
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        """Do two rectangles intersect?"""
        return (self.x1 < other.x2 and self.x2 > other.x1 and
                self.y1 < other.y2 and self.y2 > other.y1)