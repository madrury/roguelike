import tcod

from etc.enum import RoutingOptions


def get_shortest_path(game_map, source, target, routing_avoid=None):
    """Get the shortest path trhough the game map from a source to a target
    point, while avoiding certain dungeon features.

    Parameters
    ----------
    game_map: GameMap object

    source: (int, int)
      The source position.

    target: (int, int)
      The target position.

    routing_avoid: List[RoutingOptions]
      Dungeon features to avoid in the path.
      
    Returns
    -------
    path: List[(int, int)]
      The path shortest path through the game map from source to target while
      avoiding the dungeon features in routing_avoid.
    """
    walkable = make_walkable_array(game_map, routing_avoid=routing_avoid) 
    # The cell the the source and target occupy needs to manually be set to
    # walkable, else the entity will be frozen in place.
    walkable[source[0], source[1]] = True
    walkable[target[0], target[1]] = True
    pathfinder = tcod.path.AStar(walkable.T, diagonal=1.0)
    path = pathfinder.get_path(source[0], source[1], target[0], target[1])
    return path

def make_walkable_array(game_map, routing_avoid=None):
    if not routing_avoid:
        routing_avoid = []
    walkable = game_map.walkable[:, :]
    if RoutingOptions.AVOID_MONSTERS in routing_avoid:
        walkable = walkable * (1 - game_map.blocked)
    if RoutingOptions.AVOID_WATER in routing_avoid:
        walkable = walkable * (1 - game_map.water)
    if RoutingOptions.AVOID_FIRE in routing_avoid:
        walkable = walkable * (1 - game_map.fire)
    if RoutingOptions.AVOID_STEAM in routing_avoid:
        walkable = walkable * (1 - game_map.steam)
    return walkable

