import math
import random
from enum import Enum, auto
from render_functions import RenderOrder

class EntityTypes(Enum):
    PLAYER = auto()
    MONSTER = auto()
    ITEM = auto()
    CORPSE = auto()

class Entity:
    """Represents a game entity, i.e. anything that should be drawn on the map.

    Attributes
    ----------
    x: int
      The x position of the entity on the map.

    y: int
      The y position of the entity on the map.

    char: one character string.
      The symbol used to represent the entity on the map.

    color: Three tuple of integers. 
      The RGB color to draw the entity on the map.

    name: str
      The name of the entity.

    entity_type: EntityTypes object
      The type of entity.

    blocks: bool
      Does the entity block movement?

    render_order: int
      In which order shoudl the entity be rendered.  For example, the player
      should be rendered after corpses and items.

    Optional Attributes
    -------------------
    These optional attributes add custom behaviour to entities.

    attacker: Attacker object
      Manages entities attack attributes.

    harmable: Harmable object
      Manages entities HP attributes.

    ai: AI object.
      Contains AI logic for monsters.

    item: Item object
      Contains logic for using as an item.

    inventory: Inventory object.
      Contains logic for managing an inventory.
    """
    def __init__(self, x, y, char, color, name, 
                 entity_type=None,
                 render_order=RenderOrder.CORPSE,
                 blocks=False, 
                 attacker=None,
                 harmable=None,
                 ai=None,
                 item=None, 
                 inventory=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.entity_type = entity_type
        self.blocks = blocks
        self.render_order = render_order

        self.add_component(attacker, "attacker")
        self.add_component(harmable, "harmable")
        self.add_component(ai, "ai")
        self.add_component(item, "item")
        self.add_component(inventory, "inventory")

    def add_component(self, component, component_name):
        """Add a component as an attribute of the current object, and set the
        owner of the component to the current object.
        """
        if component:
            component.owner = self
        setattr(self, component_name, component)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        path = game_map.compute_path(self.x, self.y, target_x, target_y)
        dx, dy = path[0][0] - self.x, path[0][1] - self.y
        self._move_if_able(dx, dy, game_map, entities)

    def move_to_random_adjacent(self, game_map, entities):
        dx, dy = random.choice([
            (-1, 1), (0, 1), (1, 1),
            (-1, 0),         (1, 0),
            (-1, -1), (0, -1), (1, -1)]) 
        self._move_if_able(dx, dy, game_map, entities)

    def _move_if_able(self, dx, dy, game_map, entities):
        target_location = (self.x + dx, self.y + dy)
        is_walkable = game_map.walkable[target_location]
        is_blocked = get_blocking_entity_at_location(
            entities, target_location[0], target_location[1])
        if is_walkable and not is_blocked:
            self.move(dx, dy)

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx*dx + dy*dy)

    def get_closest_entity_of_type(self, entities, entity_type):
        """Get the closest entity of a given type from a list of entities."""
        closest = None
        closest_distance = math.inf
        for entity in entities:
            distance_to = self.distance_to(entity)
            if (entity.entity_type == entity_type and
                distance_to < closest_distance):
                closest = entity
                closest_distance = distance_to
        return closest


def get_blocking_entity_at_location(entities, x, y):
    """Get a blocking entity at a location, if any, from a list of entities."""
    for entity in entities:
        if entity.blocks and entity.x == x and entity.y == y:
            return entity
    return None



