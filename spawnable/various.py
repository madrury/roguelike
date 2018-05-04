import random

from colors import random_red_or_yellow
from entity import Entity
from etc.enum import EntityTypes, RenderOrder


class Fire:

    def make(x, y):
        fg_color = random_red_or_yellow()
        return Entity(
            x, y, '^',
            name="Fire",
            fg_color=fg_color,
            entity_type=EntityTypes.TERRAIN,
            render_order=RenderOrder.TERRAIN)

    def maybe_make(x, y, p=0.5):
        spawn = random.uniform(0, 1) < 0.5 
        if spawn:
            return Fire.make(x, y)
        else:
            return None
