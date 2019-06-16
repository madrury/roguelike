from utils.utils import choose_from_list_of_tuples
from etc.enum import RoutingOptions

def spawn_entities(game_map, schedule, group_definitions):
    for room in game_map.floor.rooms:
        group = choose_from_list_of_tuples(schedule)
        group_definition = group_definitions[group]
        spawn_group(game_map, group_definition, room)

def spawn_group(game_map, group_definition, room):
    for entity_type in group_definition:
        entity = spawn_in_room(game_map, entity_type, room)
        # Should this use commitable?
        if entity is not None:
            game_map.entities.append(entity)

def spawn_in_room(game_map, entity_type, room, max_tries=25):
    for _ in range(max_tries):
        x, y = room.random_point()
        if not any((x, y) == (entity.x, entity.y)
                   for entity in game_map.entities):
            entity = entity_type.make(x, y)
            break
    else:
        entity = None
    if entity and entity_can_spawn_in_space(game_map, entity, x, y):
        if entity.blocks:
            # TODO: Use commitable to change this flag.
            game_map.blocked[x, y] = True
        return entity
    else:
        return None

def entity_can_spawn_in_space(game_map, entity, x, y):
    # TODO: Should probably be a method on entity?
    return (entity.swims or not game_map.water[x, y])
