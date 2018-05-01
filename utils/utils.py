import random
import numpy as np

def choose_from_list_of_tuples(list_of_tuples):
    """Randomly sample from a catagorical distribution defined by a list
    of (probability, catagory) tuples.
    """
    probs, choices = zip(*list_of_tuples)
    return np.random.choice(choices, size=1, p=probs)[0]

def coordinates_on_circle(center, radius):
    circle = set()
    circle.update((center[0] + radius - i, center[1] + i) 
        for i in range(0, radius + 1))
    circle.update((center[0] - radius + i, center[1] - i) 
        for i in range(0, radius + 1))
    circle.update((center[0] - radius + i, center[1] + i) 
        for i in range(0, radius + 1))
    circle.update((center[0] + radius - i, center[1] - i) 
        for i in range(0, radius + 1))
    return circle

def coordinates_within_circle(center, radius):
    circle = set()
    for r in range(0, radius + 2):
        circle.update(coordinates_on_circle(center, r))
    return circle

def adjacent_coordinates(center):
        dxdy = [(-1, 1), (0, 1), (1, 1),
                (-1, 0),         (1, 0),
                (-1, -1), (0, -1), (1, -1)]
        return [(center[0] + dx, center[1] + dy) for dx, dy in dxdy]

def random_adjacent(center):
    x, y = center
    candidates = [
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1),
        (x - 1, y),                 (x + 1, y),
        (x - 1, y - 1), (x, y - 1), (x + 1, y + 1)]
    return random.choice(candidates)
