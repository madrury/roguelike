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

# TODO Transition to its own file.
#def _make_random_item(x, y, colors):
#    return Entity(x, y, '!', colors['violet'], 'Healing Potion',
#                  render_order=RenderOrder.ITEM,
#                  item=HealthPotion())
