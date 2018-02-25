import math

class Entity:

    def __init__(self, x, y, char, color, name, 
                 blocks=False, fighter=None, ai=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.fighter = fighter
        if self.fighter:
            self.fighter.owner = self
        self.ai = ai
        if self.ai:
            self.ai.owner = self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        path = game_map.compute_path(self.x, self.y, target_x, target_y)
        dx, dy = path[0][0] - self.x, path[0][1] - self.y
        is_walkable = game_map.walkable[path[0]]
        is_blocked = get_blocking_entity_at_location(
            entities, self.x + dx, self.y + dy)
        if is_walkable and not is_blocked:
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx*dx + dy*dy)

def get_blocking_entity_at_location(entities, x, y):
    for entity in entities:
        if entity.blocks and entity.x == x and entity.y == y:
            return entity
    return None
