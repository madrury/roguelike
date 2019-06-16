from utils.utils import choose_from_list_of_tuples
from etc.enum import RoutingOptions

def spawn_entities_on_floor(game_map, schedule, group_definitions):
    for room in game_map.floor.rooms:
        group = choose_from_list_of_tuples(schedule)
        group_definition = group_definitions[group]
        for entity_type in group_definition:
            spawn_in_room(game_map, entity_type, room)

def spawn_in_room(game_map, entity_type, room, max_tries=25):
    # Search for an open position in the room, one that is not already occupied
    # by some entity.
    entity = None
    for _ in range(max_tries):
        x, y = room.random_point()
        if not any((x, y) == (entity.x, entity.y) for entity in game_map.entities):
            entity = entity_type.make(x, y)
            break

    if entity and entity_can_spawn_in_space(game_map, entity, x, y):
        entity.commitable.commit(game_map)
        return entity
    else:
        return None

def entity_can_spawn_in_space(game_map, entity, x, y):
    # TODO: Should probably be a method on entity?
    return (entity.swims or not game_map.water[x, y])