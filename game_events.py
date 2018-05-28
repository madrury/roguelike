from messages import Message
from etc.colors import COLORS
from etc.enum import ResultTypes, Animations, Elements

from utils.utils import (
    get_all_entities_with_component_within_radius)


def fireblast(game_map, center, *, radius=4, damage=6, user=None):
    """Create a fireblast centered at a position of a given radius.

    The fireblast both deals damage to all enetities within the radius, and
    burns all the burnable entities within that radius.
    """
    results = []
    harmable_within_radius = (
        get_all_entities_with_component_within_radius(
            center, game_map, "harmable", radius))
    burnable_within_radius = (
        get_all_entities_with_component_within_radius(
            center, game_map, "burnable", radius))
    for entity in (x for x in harmable_within_radius if x != user):
        text = f"The {entity.name} is caught in a fireblast!"
        message = Message(text, COLORS.get('white'))
        results.append({ResultTypes.DAMAGE: (
                            entity, None, damage, [Elements.NONE]),
                        ResultTypes.MESSAGE: message})
    for entity in (x for x in burnable_within_radius if x != user):
        results.extend(entity.burnable.burn(game_map))
    results.append({
        ResultTypes.ANIMATION: (
            Animations.FIREBLAST, center, radius)})
    return results
