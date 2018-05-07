import math
import random

import tcod

from etc.enum import EntityTypes, RenderOrder


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

    name: str
      The name of the entity.

    entity_type: EntityTypes object
      The type of entity.

    fg_color: (int, int, int) RGB value
      The RGB color to draw the entity on the map.

    bg_color: (int, int, int) RGB value
      The background color to draw the entity tile, if any.

    dark_fg_color: (int, int, int) RGB value
      The RGB color to draw the entity on the map when out of view, if if any.

    dark_bg_color: (int, int, int) RGB value
      The background color to draw the entity tile when out of view, if any.

    seen: bool
      Has the player seen the entity?

    visible_out_of_fov: bool
      Should the entity be draw even when out of the players fov?

    blocks: bool
      Does the entity block movement?

    swims: bool
      Can the entity move through water spaces?

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

    shimmer: Shimmer object.
      Contains logic for changing the color of the entity according to certain
      triggers.

    burnable: Burnable object.
      Contains logic for results of attempting to burn the entity.

    spreadable: Spreadable object.
      Contains logic for an entity to self propagate across the map.
    """
    def __init__(self,
                 x, y, char, fg_color, name,
                 entity_type=None,
                 render_order=RenderOrder.CORPSE,
                 dark_fg_color=None,
                 bg_color=None,
                 dark_bg_color=None,
                 visible_out_of_fov=False,
                 seen=False,
                 blocks=False,
                 swims=False,
                 # Optional components.
                 attacker=None,
                 harmable=None,
                 ai=None,
                 item=None,
                 inventory=None,
                 swimmable=None,
                 shimmer=None,
                 burnable=None,
                 spreadable=None,
                 dissipatable=None):
        self.x = x
        self.y = y
        self.char = char
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.dark_fg_color = dark_fg_color
        self.dark_bg_color = dark_bg_color
        self.name = name
        self.entity_type = entity_type
        self.visible_out_of_fov=visible_out_of_fov
        self.seen = seen
        self.blocks = blocks
        self.swims = swims
        self.render_order = render_order

        self.add_component(attacker, "attacker")
        self.add_component(harmable, "harmable")
        self.add_component(ai, "ai")
        self.add_component(item, "item")
        self.add_component(swimmable, "swimmable")
        self.add_component(inventory, "inventory")
        self.add_component(shimmer, "shimmer")
        self.add_component(burnable, "burnable")
        self.add_component(spreadable, "spreadable")
        self.add_component(dissipatable, "dissipatable")

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
        if self.swims:
            path = game_map.compute_path(self.x, self.y, target_x, target_y)
        else:
            # TODO: Fuck all!  The path in the tcod module is transposed from
            # the Map object!
            walkable = game_map.walkable * (1 - game_map.water)
            pathfinder = tcod.path.AStar(walkable.T, diagonal=1.0)
            path = pathfinder.get_path(self.x, self.y, target_x, target_y)
            # If the entity is in a different connected component due to water,
            # then we will have an empty path.  Since the entity can SEE the
            # player, they should at least move towards them.
            if path == []:
                path = game_map.compute_path(self.x, self.y, target_x, target_y)
        if len(path) > 1:
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
        water_if_able = self.swims or not game_map.water[target_location]
        if is_walkable and not is_blocked and water_if_able:
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

    def get_n_closest_entities_of_type(self, entities, entity_type, n):
        entities_of_type = [
            e for e in entities if e.entity_type == entity_type]
        entities_of_type = sorted(
            entities_of_type, key=lambda e: self.distance_to(e))
        if len(entities_of_type) < n:
            return entities_of_type
        else:
            return entities_of_type[:n]

    def get_all_entities_of_type_within_radius(
        self, entities, entity_type, radius):
        """Get all the entities of a given type within a given range."""
        within_radius = []
        for entity in entities:
            if (self.distance_to(entity) <= radius and
                entity.entity_type == entity_type):
                within_radius.append(entity)
        return within_radius

    def get_all_entities_of_type_in_same_position(self, entities, entity_type):
        return self.get_all_entities_of_type_within_radius(
            entities, entity_type, radius=0)

    def get_all_entities_with_component_within_radius(
        self, entities, component, radius):
        """Get all the entities of a given type within a given range."""
        within_radius = []
        for entity in entities:
            if (self.distance_to(entity) <= radius and getattr(entity, component)):
                within_radius.append(entity)
        return within_radius

    def get_all_entities_with_component_in_same_position(self, entities, component):
        return self.get_all_entities_with_component_within_radius(
            entities, component, radius=0)



def get_entities_at_location(entities, x, y):
    entities_at_location = []
    for entity in entities:
        if entity.x == x and entity.y == y:
            entities_at_location.append(entity)
    return entities_at_location

def get_blocking_entity_at_location(entities, x, y):
    """Get a blocking entity at a location, if any, from a list of entities."""
    for entity in entities:
        if entity.blocks and entity.x == x and entity.y == y:
            return entity
    return None

def get_first_blocking_entity_along_path(game_map, entities, source, target):
    path = game_map.compute_path(source[0], source[1], target[0], target[1])
    for p in path:
        entity = get_blocking_entity_at_location(entities, p[0], p[1])
        if entity:
            return entity
    return None




