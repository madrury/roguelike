from utils.utils import choose_from_list_of_tuples

def spawn_entities(schedule, group_definitions, game_map, entities):
    for room in game_map.floor.rooms:
        group = choose_from_list_of_tuples(schedule)
        group_definition = group_definitions[group]
        spawn_group(group_definition, room, game_map, entities)

def spawn_group(group_definition, room, game_map, entities):
    for entity_type in group_definition:
        entity = entity_type.spawn(room, game_map, entities)
        if entity is not None:
            entities.append(entity)

def entity_can_spawn_in_space(entity, x, y, game_map):
    return entity.swims or not game_map.water[x, y]


class Spawnable:

    @classmethod
    def spawn(cls, room, game_map, entities, max_tries=25):
        for _ in range(max_tries):
            x, y = room.random_point()
            if not any((x, y) == (entity.x, entity.y) for entity in entities):
                entity = cls.make(x, y)
                break
        else:
            entity = None
        if entity and entity_can_spawn_in_space(entity, x, y, game_map):
            return entity
        else:
            return None

