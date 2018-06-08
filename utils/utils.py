import math
import random
import numpy as np

from pathfinding import make_walkable_array


def flatten_list_of_dictionaries(list_of_dictionaries):
    ret = []
    for d in list_of_dictionaries:
        for k, v in d.items():
            ret.append({k: v})
    return ret

def get_key_from_single_key_dict(d):
    return list(d)[0]

def unpack_single_key_dict(d):
    k = list(d)[0]
    return k, d[k]

def choose_from_list_of_tuples(list_of_tuples):
    """Randomly sample from a catagorical distribution defined by a list
    of (probability, catagory) tuples.
    """
    probs, choices = zip(*list_of_tuples)
    return np.random.choice(choices, size=1, p=probs)[0]

#-----------------------------------------------------------------------------
# Geometric operations.
#-----------------------------------------------------------------------------
def l2_distance(source, target):
    dx = target[0] - source[0]
    dy = target[1] - source[1]
    return math.sqrt(dx*dx + dy*dy)

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

def _bresenham_ray(game_map, source, target):
    """Bresenham's line drawing algorithm, used to draw a ray joining two
    points.

    Modified from the example at rosettacode:

    https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#Python

    Returns a list of tuples for the ray, and the index into the ray at witch
    the target position lies.
    """
    ray = []
    (x0, y0), (x1, y1) = source, target
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    idx, target_idx = 0, 0
    if dx > dy:
        err = dx / 2.0
        while game_map.within_bounds(x, y) and game_map.transparent[x, y]:
            ray.append((x, y))
            if (x, y) == target:
                target_idx = idx
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
            idx += 1
    else:
        err = dy / 2.0
        while game_map.within_bounds(x, y) and game_map.transparent[x, y]:
            ray.append((x, y))
            if (x, y) == target:
                target_idx = idx
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy  
            idx += 1
    if target_idx == 0:
        target_idx = idx
    return ray, idx, target_idx

def bresenham_line(game_map, source, target):
    ray, _, target_idx = _bresenham_ray(game_map, source, target)
    return ray[:target_idx]

def bresenham_ray(game_map, source, target):
    ray, last_idx, target_idx = _bresenham_ray(game_map, source, target)
    return ray[:last_idx]

#-----------------------------------------------------------------------------
# Choosing random map positions.
#-----------------------------------------------------------------------------
def random_adjacent(center):
    x, y = center
    candidates = [
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        (x - 1, y),                 (x + 1, y),
        (x - 1, y - 1), (x, y - 1), (x + 1, y + 1)]
    return random.choice(candidates)

def random_walkable_position(game_map, entity):
    walkable_array =  make_walkable_array(game_map, entity.routing_avoid) 
    x, y = (random.choice(range(0, game_map.width)), 
            random.choice(range(0, game_map.height)))
    while not walkable_array[x, y]:
        x, y = (random.choice(range(0, game_map.width)), 
                random.choice(range(0, game_map.height)))
    return (x, y)

#-----------------------------------------------------------------------------
# Entity Finders
#-----------------------------------------------------------------------------
def get_closest_entity_of_type(position, game_map, entity_type):
    """Get the closest entity of a given type from a list of entities."""
    closest = None
    closest_distance = math.inf
    for entity in game_map.entities:
        distance = l2_distance(position, (entity.x, entity.y))
        if (entity.entity_type == entity_type and
            distance < closest_distance):
            closest = entity
            closest_distance = distance
    return closest

def get_n_closest_entities_of_type(position, game_map, entity_type, n):
    entities_of_type = [
        e for e in game_map.entities if e.entity_type == entity_type]
    entities_of_type = sorted(
        entities_of_type, key=lambda e: l2_distance(position, (e.x, e.y)))
    if len(entities_of_type) < n:
        return entities_of_type
    else:
        return entities_of_type[:n]

def get_all_entities_of_type_within_radius(
    position, game_map, entity_type, radius):
    """Get all the entities of a given type within a given range."""
    within_radius = []
    for entity in game_map.entities:
        if (l2_distance(position, (entity.x, entity.y)) <= radius and
            entity.entity_type == entity_type):
            within_radius.append(entity)
    return within_radius

def get_all_entities_of_type_in_position(position, game_map, entity_type):
    entities = game_map.entities.get_entities_in_position(position)
    return [e for e in entities if e.entity_type == entity_type]

def get_all_entities_with_component_within_radius(
    position, game_map, component, radius):
    """Get all the entities of a given type within a given range."""
    within_radius = []
    for entity in game_map.entities:
        if (l2_distance(position, (entity.x, entity.y)) <= radius 
            and getattr(entity, component)):
            within_radius.append(entity)
    return within_radius

def get_all_entities_with_component_in_position(position, game_map, component):
    entities = game_map.entities.get_entities_in_position(position)
    return [e for e in entities if getattr(e, component)]

def get_blocking_entity_in_position(game_map, position):
    entities = game_map.entities.get_entities_in_position(position)
    blockers = [e for e in entities if e.blocks]
    if len(blockers) >= 2:
        raise RuntimeError(
            f"More than one blocking entity {blockers[0].name, blockers[1].name}"
             "in position {position}")
    if blockers == []:
        return None
    entity = blockers[0]
    if entity.blocks:
        return entity

def get_first_blocking_entity_along_path(game_map, source, target):
    path = bresenham_ray(
        game_map, (source[0], source[1]), (target[0], target[1]))
    for p in path[1:]:
        entity = get_blocking_entity_in_position(game_map, (p[0], p[1]))
        if entity:
            return entity
    return None
