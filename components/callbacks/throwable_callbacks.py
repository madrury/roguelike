from messages import Message
from etc.enum import ResultTypes, CursorTypes, Animations, Elements

from etc.colors import COLORS
from etc.game_config import (
    HEALTH_POTION_HP_INCREASE_AMOUNT,
    THROWING_KNIFE_BASE_DAMAGE,
    THROWN_WEAPON_DAMAGE_FACTOR)

from utils.utils import get_first_blocking_entity_along_ray


class HealthPotionCallback:
    """Throw a health potion towards the selected position."""
    def __init__(self, owner, game_map, user):
        self.owner = owner
        self.game_map = game_map
        self.user = user

    def execute(self, x, y):
        results = []
        target = get_first_blocking_entity_along_ray(
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
                ResultTypes.INCREASE_MAX_HP: (
                    target, HEALTH_POTION_HP_INCREASE_AMOUNT),
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


class ConfusionPotionCallback:
    """Throw a confusion potion towards the selected position."""
    def __init__(self, owner, game_map, user):
        self.owner = owner
        self.game_map = game_map
        self.user = user

    def execute(self, x, y):
        results = []
        target = get_first_blocking_entity_along_ray(
            self.game_map, (self.user.x, self.user.y), (x, y))
        if target:
            text = f"{target.name} becomes confused!"
            throw_animation = (
                Animations.THROW_POTION,
                (self.user.x, self.user.y), (target.x, target.y))
            potion_animation = (
                Animations.CONFUSION_POTION, (target.x, target.y))
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.CONFUSE: target,
                ResultTypes.ANIMATION: (
                    Animations.CONCATINATED, (throw_animation, potion_animation))
            }),
        else:
            text = "The confusion potion splashes on the ground."
            throw_animation = (
                Animations.THROW_POTION, (self.user.x, self.user.y), (x, y))
            spill_animation = (Animations.CONFUSION_POTION, (x, y))
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.ANIMATION: (
                    Animations.CONCATINATED, (throw_animation, spill_animation))
            })
        return results

        
class WeaponCallback:
    """Throw a weapong towards the target square."""
    def __init__(self, owner, game_map, user):
        self.owner = owner
        self.game_map = game_map
        self.user = user

    def execute(self, x, y):
        results = []
        monster = get_first_blocking_entity_along_ray(
            self.game_map, (self.user.x, self.user.y), (x, y))
        if monster and monster.harmable:
            text = f"The {self.owner.owner.name} pierces the {monster.name}'s flesh."
            results.append({
                ResultTypes.MESSAGE: Message(text, COLORS.get('white')),
                ResultTypes.DAMAGE: (
                    monster, None, 
                    THROWN_WEAPON_DAMAGE_FACTOR * self.owner.owner.stats.power,
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


class ThrowingKnifeCallback:
    """Throw a knife towards the selected postion."""
    def __init__(self, owner, game_map, user):
        self.owner = owner
        self.game_map = game_map
        self.user = user

    def execute(self, x, y):
        results = []
        monster = get_first_blocking_entity_along_ray(
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
