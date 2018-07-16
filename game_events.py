from messages import Message

from game_objects.terrain import Water

from etc.colors import COLORS
from etc.enum import ResultTypes, Animations, Elements, EntityTypes, CursorTypes
from utils.utils import (
    coordinates_within_circle,
    get_all_entities_of_type_within_radius,
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


def waterblast(game_map, center, *, radius=4, damage=6, user=None):
    """Create a blast of water centered at a position of a given radius.

    The waterblast both deals damage, and floods all tiles within a given
    radius.
    """
    results = []
    harmable_within_radius = (
        get_all_entities_with_component_within_radius(
            center, game_map, "harmable", radius))
    for entity in (x for x in harmable_within_radius if x != user):
        text = f"The {entity.name} is caught in a waterblast!"
        message = Message(text, COLORS.get('white'))
        results.append({ResultTypes.DAMAGE: (
                            entity, None, damage, [Elements.WATER]),
                        ResultTypes.MESSAGE: message})
    blast_coordinates = coordinates_within_circle(center, radius)
    for coord in blast_coordinates:
        if game_map.walkable[coord]:
            entities = get_all_entities_of_type_within_radius(
                coord, game_map, EntityTypes.TERRAIN, 0)
            for entity in entities:
                results.append({ResultTypes.REMOVE_ENTITY: entity})
            water = Water.make(game_map, coord[0], coord[1])
            results.append({ResultTypes.ADD_ENTITY: water})
    results.append({
        ResultTypes.ANIMATION: (
            Animations.WATERBLAST, center, radius)})
    return results


def use_staff(staff_usable, callback_cls, game_map, user):
    """Generic function for using a staff.

    Parameters
    ----------
    staff_usable: Usable component.
        The usable component of the item entity.

    callback_cls:
        Class to use for the callback after the position to use the staff has
        been selected.

    game_map: GameMap
        The current game map.

    user: Entity
        The entity that used the staff.
    """
    if staff_usable.owner.consumable.uses > 0:
        callback = callback_cls(staff_usable, game_map, user)
        return [{
            ResultTypes.CURSOR_MODE: (
                user.x, user.y, callback, CursorTypes.RAY)}]
    else:
        message = Message(f"Cannot use {staff_usable.owner.name} with zero charges.")
        return [{
            ResultTypes.MESSAGE: message}]
