from utils.utils import coordinates_within_circle

class Illuminatable:

    def __init__(self, radius=3):
        self.radius = radius

    def illuminate(self, game_map):
        center = (self.owner.x, self.owner.y)
        for x, y in coordinates_within_circle(center, self.radius):
            print(x, y)
            if game_map.within_bounds(x, y):
                game_map.illuminated[x, y] = True
