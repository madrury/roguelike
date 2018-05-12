from entity import Entity

from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups

from components.usable import (
    NullUsable, HealthPotionUsable, MagicMissileUsable, FireblastUsable)
from components.throwable import (
    NullThrowable, HealthPotionThrowable, ThrowingKnifeThrowable)
from components.burnable import ItemBurnable


class HealthPotion:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '!', COLORS['violet'], 'Potion of Health',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      usable=HealthPotionUsable(),
                      throwable=HealthPotionThrowable())


class MagicMissileScroll:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Magic Missile',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      burnable=ItemBurnable(),
                      usable=MagicMissileUsable(),
                      throwable=NullThrowable())


class FireblastScroll:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Fireblast',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      burnable=ItemBurnable(),
                      usable=FireblastUsable(),
                      throwable=NullThrowable())


class ThrowingKnife:

    @staticmethod
    def make(x, y):
        return Entity(x, y, chr(24), COLORS['white'], 'Throwing Knife',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      usable=NullUsable(),
                      throwable=ThrowingKnifeThrowable())
