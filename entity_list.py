class EntityList:
    """A data structure for contining all the entities in a current map.  This
    is designed to support two sets of operations:

      - Standard list methods: append, remove, and iteration.
      - Efficient lookup by position in the map.
    """
    def __init__(self, width, height):
        self.lst = []
        #self.coordinate_map = {
        #    (i, j): [] for i, j in itertools.product(range(width), range(height)
        #}

    def append(self, entity):
        self.lst.append(entity)

    def remove(self, entitiy):
        self.lst.remove(entitiy)

    def __iter__(self):
        yield from iter(self.lst)

