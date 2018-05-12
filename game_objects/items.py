from entity import Entity

from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups
from components.item import (
    MagicMissileComponent,
    FireblastComponent, ThrowingKnifeComponent)

from components.usable import HealthPotionUsable
from components.throwable import HealthPotionThrowable
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
                      item=MagicMissileComponent(),
                      burnable=ItemBurnable())


class FireblastScroll:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Fireblast',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      item=FireblastComponent(),
                      burnable=ItemBurnable())


class ThrowingKnife:

    @staticmethod
    def make(x, y):
        return Entity(x, y, chr(24), COLORS['white'], 'Throwing Knife',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      item=ThrowingKnifeComponent())
