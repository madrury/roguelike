import math
import random
import numpy as np

def choose_from_list_of_tuples(list_of_tuples):
    """Randomly sample from a catagorical distribution defined by a list
    of (probability, catagory) tuples.
    """
    probs, choices = zip(*list_of_tuples)
    return np.random.choice(choices, size=1, p=probs)[0]

def coordinates_on_circle(center, radius):
    circle = set()
    circle.update((center[0] + radius - i, center[1] + i) 
        for i in range(0, radius + 1))
    circle.update((center[0] - radius + i, center[1] - i) 
        for i in range(0, radius + 1))
    circle.update((center[0] - radius + i, center[1] + i) 
        for i in range(0, radius + 1))
    circle.update((center[0] + radius - i, center[1] - i) 
        for i in range(0, radius + 1))
    return circle

def coordinates_within_circle(center, radius):
    circle = set()
    for r in range(0, radius + 2):
        circle.update(coordinates_on_circle(center, r))
    return circle

def adjacent_coordinates(center):
        dxdy = [(-1, 1), (0, 1), (1, 1),
                (-1, 0),         (1, 0),
                (-1, -1), (0, -1), (1, -1)]
        return [(center[0] + dx, center[1] + dy) for dx, dy in dxdy]

def random_adjacent(center):
    x, y = center
    candidates = [
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        (x - 1, y),                 (x + 1, y),
        (x - 1, y - 1), (x, y - 1), (x + 1, y + 1)]
    return random.choice(candidates)

#-----------------------------------------------------------------------------
# Entity Finders
#-----------------------------------------------------------------------------
def distance_to(source, target):
    dx = target[0] - source[0]
    dy = target[1] - source[1]
    return math.sqrt(dx*dx + dy*dy)

def get_closest_entity_of_type(position, game_map, entity_type):
    """Get the closest entity of a given type from a list of entities."""
    closest = None
    closest_distance = math.inf
    for entity in game_map.entities:
        distance_to = distance_to(position, (entity.x, entity.y))
        if (entity.entity_type == entity_type and
            distance_to < closest_distance):
            closest = entity
            closest_distance = distance_to
    return closest

def get_n_closest_entities_of_type(position, game_map, entity_type, n):
    entities_of_type = [
        e for e in game_map.entities if e.entity_type == entity_type]
    entities_of_type = sorted(
        entities_of_type, key=lambda e: distance_to(position, (e.x, e.y)))
    if len(entities_of_type) < n:
        return entities_of_type
    else:
        return entities_of_type[:n]

def get_all_entities_of_type_within_radius(
    position, game_map, entity_type, radius):
    """Get all the entities of a given type within a given range."""
    within_radius = []
    for entity in game_map.entities:
        if (distance_to(position, (entity.x, entity.y)) <= radius and
            entity.entity_type == entity_type):
            within_radius.append(entity)
    return within_radius

def get_all_entities_of_type_in_position(position, game_map, entity_type):
    return get_all_entities_of_type_within_radius(
        position, game_map, entity_type, radius=0)

def get_all_entities_with_component_within_radius(
    position, game_map, component, radius):
    """Get all the entities of a given type within a given range."""
    within_radius = []
    for entity in game_map.entities:
        if (distance_to(position, (entity.x, entity.y)) <= radius 
            and getattr(entity, component)):
            within_radius.append(entity)
    return within_radius

def get_all_entities_with_component_in_position(position, game_map, component):
    return get_all_entities_with_component_within_radius(
        position, game_map, component, radius=0)

def get_entities_at_location(game_map, x, y):
    entities_at_location = []
    for entity in game_map.entities:
        if entity.x == x and entity.y == y:
            entities_at_location.append(entity)
    return entities_at_location

def get_blocking_entity_at_location(game_map, x, y):
    """Get a blocking entity at a location, if any, from a list of entities."""
    for entity in game_map.entities:
        if entity.blocks and entity.x == x and entity.y == y:
            return entity
    return None

def get_first_blocking_entity_along_path(game_map, source, target):
    path = game_map.compute_path(source[0], source[1], target[0], target[1])
    for p in path:
        entity = get_blocking_entity_at_location(game_map, p[0], p[1])
        if entity:
            return entity
    return None
