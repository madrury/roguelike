import math
from render_functions import RenderOrder


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

    block: bool
      Does the entity block movement?

    render_order: int
      In which order shoudl the entity be rendered.  For example, the player
      should be rendered after corpses and items.

    Optional Attributes
    -------------------
    These optional attributes add custom behaviour to entities.

    fighter: Fighter object
      Manages entities HP and attack attributes.

    ai: AI object.
      Contains AI logic for monsters.

    item: Item object
      Contains logic for using as an item.

    inventory: Inventory object.
      Contains logic for managing an inventory.
    """
    def __init__(self, x, y, char, color, name, 
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
        # TODO: Maybe the game map should own this logic?
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
