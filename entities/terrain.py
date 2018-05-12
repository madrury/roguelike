from entity import Entity
from colors import random_light_green, random_light_water, random_dark_water
from etc.enum import Terrain, EntityTypes, RenderOrder
from etc.colors import COLORS
from components.shimmer import WaterShimmer
from components.burnable import GrassBurnable, WaterBurnable

class Water:

    @staticmethod
    def make(x, y):
        fg_color = random_light_water()
        bg_color = random_light_water()
        dark_fg_color = random_dark_water()
        dark_bg_color = random_dark_water()
        return Entity(
            x, y, '~',
            name="Water",
            fg_color=fg_color,
            dark_fg_color=dark_fg_color,
            bg_color=bg_color,
            dark_bg_color=dark_bg_color,
            visible_out_of_fov=True,
            entity_type=EntityTypes.TERRAIN,
            render_order=RenderOrder.TERRAIN,
            shimmer=WaterShimmer(),
            burnable=WaterBurnable())
