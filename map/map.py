from tdl.map import Map
import numpy as np
from random import randint, choice

class GameMap(Map):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.explored = np.zeros((width, height)).astype(bool)

    def make_transparent_and_walkable(self, x, y):
        self.walkable[x, y] = True
        self.transparent[x, y] = True
