from entity import Entity

from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups

from components.burnable import ItemBurnable
from components.consumable import Consumable
from components.commitable import BaseCommitable
from components.usable import (
    NullUsable, HealthPotionUsable, MagicMissileUsable, FireblastUsable,
    TorchUsable)
from components.throwable import (
    NullThrowable, HealthPotionThrowable, ThrowingKnifeThrowable)


class HealthPotion:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '!', COLORS['violet'], 'Potion of Health',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      usable=HealthPotionUsable(),
                      throwable=HealthPotionThrowable())


class MagicMissileScroll:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Magic Missile',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      burnable=ItemBurnable(),
                      usable=MagicMissileUsable(),
                      throwable=NullThrowable())


class FireblastScroll:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Fireblast',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      burnable=ItemBurnable(),
                      usable=FireblastUsable(),
                      throwable=NullThrowable())


class ThrowingKnife:

    @staticmethod
    def make(x, y):
        return Entity(x, y, chr(24), COLORS['violet'], 'Throwing Knife',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      consumable=Consumable(uses=5),
                      usable=NullUsable(),
                      throwable=ThrowingKnifeThrowable())


class Torch:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '/', COLORS['violet'], 'Torch',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      usable=TorchUsable(),
                      throwable=NullThrowable())
