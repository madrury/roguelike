from utils.utils import choose_from_list_of_tuples

def spawn_entities(schedule, group_definitions, floor, entities):
    for room in floor.rooms:
        group = choose_from_list_of_tuples(schedule)
        group_definition = group_definitions[group]
        spawn_group(group_definition, room, entities)

def spawn_group(group_definition, room, entities):
    for entity_type in group_definition:
        entity = entity_type.spawn(room, entities)
        if entity is not None:
            entities.append(entity)


class Spawnable:

    @classmethod
    def spawn(cls, room, entities, max_tries=25):
        for _ in range(max_tries):
            x, y = room.random_point()
            if not any((x, y) == (entity.x, entity.y) for entity in entities):
                entity = cls.make(x, y)
                break
        else:
            entity = None
        return entity

