from messages import Message

from etc.colors import COLORS
from etc.enum import ResultTypes, CursorTypes, Animations, Elements
from etc.game_config import (
    HEALTH_POTION_HEAL_AMOUNT, THROWING_KNIFE_BASE_DAMAGE,
    THROWN_WEAPON_DAMAGE_FACTOR)

from utils.utils import get_first_blocking_entity_along_path


class NullThrowable:

    def throw(self, game_map, throw):
        return []

    def __bool__(self):
        return False


class HealthPotionThrowable:

    def __init__(self, healing=HEALTH_POTION_HEAL_AMOUNT):
        self.name = "Healing Potion"
        self.healing = healing

    def throw(self, game_map, thrower):
        """Throw the health potion at a target."""
        callback = HealthPotionCallback(self, game_map, thrower)
        return [
            {ResultTypes.CURSOR_MODE: (
                thrower.x, thrower.y, callback, CursorTypes.PATH)}]


class HealthPotionCallback:
    """A callback for managing throwing a health poition.
    
    Called after the player enters a cursor selection.
    """
    def __init__(self, owner, game_map, user):
        self.owner = owner
        self.game_map = game_map
        self.user = user

    def execute(self, x, y):
        results = []
        target = get_first_blocking_entity_along_path(
            self.game_map, (self.user.x, self.user.y), (x, y))
        if target:
            text = "The health potion heals the {}'s wounds".format(
                target.name)
            throw_animation = (
                Animations.THROW_POTION,
                (self.user.x, self.user.y), (target.x, target.y))
            heal_animation = (
                Animations.HEALTH_POTION, (target.x, target.y))
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.DAMAGE: (
                    target, None, -self.owner.healing, [Elements.HEALING]),
                ResultTypes.ANIMATION: (
                    Animations.CONCATINATED, (throw_animation, heal_animation))
            }),
        else:
            text = "The health potion splashes on the ground."
            throw_animation = (
                Animations.THROW_POTION, (self.user.x, self.user.y), (x, y))
            spill_animation = (Animations.HEALTH_POTION, (x, y))
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.ANIMATION: (
                    Animations.CONCATINATED, (throw_animation, spill_animation))
            })
        return results


class WeaponThrowable:

    def throw(self, game_map, user):
        callback = WeaponCallback(self, game_map, user)
        return [
            {ResultTypes.CURSOR_MODE: (
                user.x, user.y, callback, CursorTypes.PATH)}]


class WeaponCallback:

    def __init__(self, owner, game_map, user):
        self.owner = owner
        self.game_map = game_map
        self.user = user

    def execute(self, x, y):
        results = []
        monster = get_first_blocking_entity_along_path(
            self.game_map, (self.user.x, self.user.y), (x, y))
        if monster and monster.harmable:
            text = f"The {self.owner.owner.name} pierces the {monster.name}'s flesh."
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.DAMAGE: (
                    monster, None, 
                    10*self.owner.owner.stats.power,
                    self.owner.owner.stats.elements),
                ResultTypes.ANIMATION: (
                    Animations.THROWING_KNIFE,
                    (self.user.x, self.user.y),
                    (monster.x, monster.y))
            })
        else:
            # Todo: Have the knife drop on the ground.
            text = "The {self.owner.name} clatters to the ground"
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
            })
        return results
        

class ThrowingKnifeThrowable:

    def __init__(self, damage=THROWING_KNIFE_BASE_DAMAGE):
        self.damage = damage

    def throw(self, game_map, user):
        callback = ThrowingKnifeCallback(self, game_map, user)
        return [
            {ResultTypes.CURSOR_MODE: (
                user.x, user.y, callback, CursorTypes.PATH)}]


class ThrowingKnifeCallback:
    """A callback for managing throwing a health poition.
    
    Called after the player enters a cursor selection.
    """
    def __init__(self, owner, game_map, user):
        self.owner = owner
        self.game_map = game_map
        self.user = user

    def execute(self, x, y):
        results = []
        monster = get_first_blocking_entity_along_path(
            self.game_map, (self.user.x, self.user.y), (x, y))
        if monster and monster.harmable:
            text = f"The throwing knife pierces the {monster.name}'s flesh."
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.DAMAGE: (monster, None, self.owner.damage, [Elements.NONE]),
                ResultTypes.ANIMATION: (
                    Animations.THROWING_KNIFE,
                    (self.user.x, self.user.y),
                    (monster.x, monster.y))
            })
        else:
            # Todo: Have the knife drop on the ground.
            text = "The throwing knife clatters to the ground"
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
            })
        return results
