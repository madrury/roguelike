from utils.utils import coordinates_within_circle


class Illuminatable:
    """Component for objects that illuminate their surroundings.

    Illumination causes areas of the game map to be visible even when not in
    the players fov.  An object with this component will make an area within a
    radius of itself always visible.
    """
    def __init__(self, radius=3):
        self.radius = radius

    def illuminate(self, game_map):
        center = (self.owner.x, self.owner.y)
        for x, y in coordinates_within_circle(center, self.radius):
            if game_map.within_bounds(x, y):
                game_map.illuminated[x, y] = True
