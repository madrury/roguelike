from colors import random_light_water, random_dark_water

class WaterShimmer:
    """Change the random colors of a water tile."""

    def shimmer(self):
        self.owner.fg_color = random_light_water()
        self.owner.bg_color = random_light_water()
        self.owner.dark_fg_color = random_dark_water()
        self.ownerdark_bg_color = random_dark_water()
