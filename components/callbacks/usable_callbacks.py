from etc.enum import ResultTypes, Animations
from utils.utils import (
    bresenham_ray, get_all_entities_with_component_in_position)


class TorchCallback:
    """Burn all entities in the selected position."""
    def __init__(self, owner, game_map, user):
        self.owner = owner
        self.game_map = game_map
        self.user = user

    def execute(self, x, y):
        results = []
        burnable_entities = get_all_entities_with_component_in_position(
            (x, y), self.game_map, "burnable")
        for entity in burnable_entities:
            results.extend(entity.burnable.burn(self.game_map))
        return results


class FireStaffCallback:
    """Draw the ray through the user and the selected position.  Burn all
    entities along this ray until the first blocking entity encountered.
    """
    def __init__(self, owner, game_map, user):
        self.owner = owner
        self.game_map = game_map
        self.user = user

    def execute(self, x, y):
        results = []
        source, target = (self.user.x, self.user.y), (x, y)
        ray = bresenham_ray(self.game_map, source, target)
        last_position = ray[-1]
        for position in ray[1:]:
            burnable_entities = get_all_entities_with_component_in_position(
                position, self.game_map, "burnable")
            for entity in burnable_entities:
                results.extend(entity.burnable.burn(self.game_map))
            entities_in_position = (
                self.game_map.entities.get_entities_in_position(position))
            if any(entity.blocks for entity in entities_in_position):
                last_position = position
                break
        results.append({
            ResultTypes.ANIMATION: (
                Animations.FIREBALL, source, last_position)})
        return results
