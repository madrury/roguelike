from etc.colors import COLORS

def highlight_array(array, game_map, color):
    for x in range(array.shape[0]):
        for y in range(array.shape[1]):
            if array[x, y]:
                game_map.highlight_position(x, y, color)
