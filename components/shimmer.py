from colors import (
    random_light_water, random_dark_water, 
    random_light_ice, random_dark_ice,
    random_red_or_yellow, random_grey)

class WaterShimmer:
    """Change the random colors of a water tile."""
    def shimmer(self):
        self.owner.fg_color = random_light_water()
        self.owner.bg_color = random_light_water()
        self.owner.dark_fg_color = random_dark_water()
        self.ownerdark_bg_color = random_dark_water()


class IceShimmer:
    """Change the random colors of an ice tile."""
    def shimmer(self):
        self.owner.fg_color = random_light_ice()
        self.owner.bg_color = random_light_ice()
        self.owner.dark_fg_color = random_dark_ice()
        self.ownerdark_bg_color = random_dark_ice()
       


class FireShimmer:
    """Change the random colors of a fire tile."""
    def shimmer(self):
        self.owner.fg_color = random_red_or_yellow()
        self.owner.bg_color = random_red_or_yellow()


class SteamShimmer:
    """Change the random colors of a steam tile."""
    def shimmer(self):
        self.owner.fg_color = random_grey()
        self.owner.bg_color = random_grey()
