from utils.utils import choose_from_list_of_tuples
from etc.enum import RoutingOptions


def spawn_entities(schedule, group_definitions, game_map):
    for room in game_map.floor.rooms:
        group = choose_from_list_of_tuples(schedule)
        group_definition = group_definitions[group]
        spawn_group(group_definition, room, game_map)

def spawn_group(group_definition, room, game_map):
    for entity_type in group_definition:
        entity = spawn_in_room(entity_type, room, game_map)
        if entity is not None:
            game_map.entities.append(entity)

def spawn_in_room(entity_type, room, game_map, max_tries=25):
    for _ in range(max_tries):
        x, y = room.random_point()
        if not any((x, y) == (entity.x, entity.y)
                   for entity in game_map.entities):
            entity = entity_type.make(x, y)
            break
    else:
        entity = None
    if entity and entity_can_spawn_in_space(entity, x, y, game_map):
        if entity.blocks:
            # TODO: Use commitable to change this flag.
            game_map.blocked[x, y] = True
        return entity
    else:
        return None

def entity_can_spawn_in_space(entity, x, y, game_map):
    return (entity.swims or not game_map.water[x, y])
