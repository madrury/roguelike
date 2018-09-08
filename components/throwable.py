from etc.enum import ResultTypes, CursorTypes

from etc.game_config import (
    HEALTH_POTION_HEAL_AMOUNT, THROWING_KNIFE_BASE_DAMAGE)

from components.callbacks.throwable_callbacks import (
    HealthPotionCallback, ConfusionPotionCallback, SpeedPotionCallback,
    WeaponCallback, ThrowingKnifeCallback)


class NullThrowable:

    def throw(self, game_map, throw):
        return []

    def __bool__(self):
        return False


class HealthPotionThrowable:
    """Throw a health potion at a target."""
    def __init__(self, healing=HEALTH_POTION_HEAL_AMOUNT):
        self.name = "Healing Potion"
        self.healing = healing

    def throw(self, game_map, thrower):
        callback = HealthPotionCallback(self, game_map, thrower)
        return [{
            ResultTypes.CURSOR_MODE: (
                thrower.x, thrower.y, callback, CursorTypes.PATH)}]


class ConfusionPotionThrowable:
    """Throw a potion of confusion at a target."""
    def __init__(self):
        self.name = "Potion of Confusion"

    def throw(self, game_map, thrower):
        callback = ConfusionPotionCallback(self, game_map, thrower)
        return [{
            ResultTypes.CURSOR_MODE: (
                thrower.x, thrower.y, callback, CursorTypes.PATH)}]


class SpeedPotionThrowable:
    """Throw a potion of speed at a target."""
    def __init__(self):
        self.name = "Potion of Speed"

    def throw(self, game_map, thrower):
        callback = SpeedPotionCallback(self, game_map, thrower)
        return [{
            ResultTypes.CURSOR_MODE: (
                thrower.x, thrower.y, callback, CursorTypes.PATH)}]


class WeaponThrowable:
    """Throw a weapon at a target.  Does damage equal to a multiple of weapon
    strength.
    """
    def throw(self, game_map, user):
        callback = WeaponCallback(self, game_map, user)
        return [{ResultTypes.CURSOR_MODE: (
            user.x, user.y, callback, CursorTypes.PATH)}]


class ThrowingKnifeThrowable:
    """Throw a knife at a target."""
    def __init__(self, damage=THROWING_KNIFE_BASE_DAMAGE):
        self.damage = damage

    def throw(self, game_map, user):
        callback = ThrowingKnifeCallback(self, game_map, user)
        return [
            {ResultTypes.CURSOR_MODE: (
                user.x, user.y, callback, CursorTypes.PATH)}]


