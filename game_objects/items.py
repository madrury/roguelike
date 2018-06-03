from entity import Entity

from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups

from components.burnable import ItemBurnable
from components.consumable import FinitelyConsumable, InfinitelyConsumable
from components.commitable import BaseCommitable
from components.floatable import Floatable
from components.movable import Movable
from components.usable import (
    NullUsable, HealthPotionUsable, PowerPotionUsable, MagicMissileUsable,
    FireblastUsable, TorchUsable, WaterblastUsable)
from components.throwable import (
    NullThrowable, HealthPotionThrowable, ThrowingKnifeThrowable)


class HealthPotion:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '!', COLORS['violet'], 'Potion of Health',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(uses=1),
                      floatable=Floatable(),
                      movable=Movable(),
                      usable=HealthPotionUsable(),
                      throwable=HealthPotionThrowable())


class PowerPotion:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '!', COLORS['violet'], 'Potion of Power',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(uses=1),
                      floatable=Floatable(),
                      movable=Movable(),
                      usable=PowerPotionUsable())


class MagicMissileScroll:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Magic Missile',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      burnable=ItemBurnable(),
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(uses=1),
                      floatable=Floatable(),
                      movable=Movable(),
                      usable=MagicMissileUsable(),
                      throwable=NullThrowable())


class FireblastScroll:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Fireblast',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      burnable=ItemBurnable(),
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(uses=1),
                      floatable=Floatable(),
                      movable=Movable(),
                      usable=FireblastUsable(),
                      throwable=NullThrowable())


class WaterblastScroll:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Waterblast',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      burnable=ItemBurnable(),
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(uses=1),
                      floatable=Floatable(),
                      movable=Movable(),
                      usable=WaterblastUsable(),
                      throwable=NullThrowable())


class ThrowingKnife:

    @staticmethod
    def make(x, y):
        return Entity(x, y, chr(24), COLORS['violet'], 'Throwing Knife',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(uses=5),
                      floatable=Floatable(),
                      movable=Movable(),
                      usable=NullUsable(),
                      throwable=ThrowingKnifeThrowable())


class Torch:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '/', COLORS['violet'], 'Torch',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      consumable=InfinitelyConsumable(),
                      floatable=Floatable(),
                      movable=Movable(),
                      usable=TorchUsable(),
                      throwable=NullThrowable())
