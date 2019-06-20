from itertools import product

from etc.colors import COLORS


def highlight_array(array, game_map, color):
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            if array[x, y]:
                game_map.highlight_position(x, y, color)

def highlight_stairs(game_map, color):
    if game_map.upward_stairs_position:
        game_map.highlight_position(*game_map.upward_stairs_position, color)
    if game_map.downward_stairs_position:
        game_map.highlight_position(*game_map.downward_stairs_position, color)

def highlight_rooms(game_map, color):
    for room in game_map.floor.rooms:
        for i, j in product(range(room.width), range(room.height)):
            if room.layout[i, j]:
                game_map.highlight_position(i + room.x, j + room.y, color)

def draw_dijkstra_map(dm, game_map):
    xmax, ymax = dm.dmap.shape
    for x in range(0, xmax):
        for y in range(0, ymax):
            if dm.dmap[x, y] != dm.initial:
                n = int(min(dm.dmap[x, y], 9))
                game_map.draw_char(
                    x, y, str(n),
                    fg=COLORS["black"],
                    bg=game_map.bg_colors[x, y])

def draw_dijkstra_map_of_radius(game_map, player, radius=4):
        from pathfinding import make_walkable_array
        from etc.enum import RoutingOptions
        from utils.debug import draw_dijkstra_map
        from dijkstra_map.dijkstra_map import DijkstraMap
        walkable = make_walkable_array(game_map,
            routing_avoid=[RoutingOptions.AVOID_WATER,
                           RoutingOptions.AVOID_FIRE,
                           RoutingOptions.AVOID_MONSTERS,
                           RoutingOptions.AVOID_STEAM])
        dm = DijkstraMap(walkable)
        dm.set_square_sources((player.x, player.y), radius)
        dm.build()
        draw_dijkstra_map(dm, game_map)
