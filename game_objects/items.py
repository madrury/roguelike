from entity import Entity

from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups
from etc.game_config import (
    THROWING_KNIFE_BASE_USES, STAFF_BASE_USES, STAFF_RECHARGE_TIME)

from components.burnable import ItemBurnable
from components.consumable import FinitelyConsumable, InfinitelyConsumable
from components.commitable import BaseCommitable
from components.floatable import Floatable
from components.movable import Movable
from components.rechargeable import Rechargeable
from components.usable import (
    NullUsable, HealthPotionUsable, PowerPotionUsable, ConfusionPotionUsable,
    SpeedPotionUsable, TeleportationPotionUsable, MagicMissileUsable,
    FireblastUsable, TorchUsable, WaterblastUsable, FireStaffUsable,
    IceStaffUsable)
from components.throwable import (
    NullThrowable, HealthPotionThrowable, ConfusionPotionThrowable, 
    TeleportationPotionThrowable, SpeedPotionThrowable, ThrowingKnifeThrowable)


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


class ConfusionPotion:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '!', COLORS['violet'], 'Potion of Confusion',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(uses=1),
                      floatable=Floatable(),
                      movable=Movable(),
                      usable=ConfusionPotionUsable(),
                      throwable=ConfusionPotionThrowable())


class SpeedPotion:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '!', COLORS['violet'], 'Potion of Speed',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(uses=1),
                      floatable=Floatable(),
                      movable=Movable(),
                      usable=SpeedPotionUsable(),
                      throwable=SpeedPotionThrowable())


class TeleportationPotion:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '!', COLORS['violet'], 'Potion of Teleportation',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(uses=1),
                      floatable=Floatable(),
                      movable=Movable(),
                      usable=TeleportationPotionUsable(),
                      throwable=TeleportationPotionThrowable())


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
                      consumable=FinitelyConsumable(
                          uses=THROWING_KNIFE_BASE_USES),
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


class FireStaff:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '/', COLORS['violet'], 'Fire Staff',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(
                          uses=STAFF_BASE_USES, 
                          discard_on_empty=False,
                          display_on_one=True),
                      floatable=Floatable(),
                      movable=Movable(),
                      rechargeable=Rechargeable(
                          charges_needed=STAFF_RECHARGE_TIME),
                      usable=FireStaffUsable(),
                      throwable=NullThrowable())

class IceStaff:

    @staticmethod
    def make(x, y):
        return Entity(x, y, '/', COLORS['violet'], 'Ice Staff',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      consumable=FinitelyConsumable(
                          uses=STAFF_BASE_USES, 
                          discard_on_empty=False,
                          display_on_one=True),
                      floatable=Floatable(),
                      movable=Movable(),
                      rechargeable=Rechargeable(
                          charges_needed=STAFF_RECHARGE_TIME),
                      usable=IceStaffUsable(),
                      throwable=NullThrowable())
