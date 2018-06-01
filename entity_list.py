import itertools


class EntityList:
    """A data structure for contining all the entities in a current map.  This
    is designed to support two sets of operations:

      - Standard list methods: append, remove, and iteration.
      - Efficient lookup by position in the map.
    """
    def __init__(self, width, height):
        self.lst = []
        self.coordinate_map = {
            (i, j): [] for i, j in itertools.product(range(width), range(height))
        }

    def append(self, entity):
        self.lst.append(entity)
        self.coordinate_map[(entity.x, entity.y)].append(entity)

    def remove(self, entity):
        self.lst.remove(entity)
        self.coordinate_map[(entity.x, entity.y)].remove(entity)

    def update_position(self, entity, old_position, new_position):
        self.coordinate_map[old_position].remove(entity)
        self.coordinate_map[new_position].append(entity)

    def get_entities_in_position(self, position):
        return self.coordinate_map[position]

    def __iter__(self):
        yield from self.lst
