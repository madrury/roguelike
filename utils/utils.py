import numpy as np

def choose_from_list_of_tuples(list_of_tuples):
    """Randomly sample from a catagorical distribution defined by a list
    of (probability, catagory) tuples.
    """
    probs, choices = zip(*list_of_tuples)
    return np.random.choice(choices, size=1, p=probs)[0]

def coordinates_on_circle(center, radius):
    circle = set()
    circle.update((radius - i, i) for i in range(0, radius + 1))
    circle.update((-radius + i, -i) for i in range(0, radius + 1))
    circle.update((-radius + i, i) for i in range(0, radius + 1))
    circle.update((radius - i, -i) for i in range(0, radius + 1))
    return circle

def coordinates_within_circle(center, radius):
    circle = set()
    for r in range(radius + 1):
        circle.update(coordinates_on_circle(center, radius))
    return circle
