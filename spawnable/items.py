from entity import Entity

from spawnable.spawnable import Spawnable
from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups
from components.item import (
    HealthPotionComponent, MagicMissileComponent,
    FireblastComponent, ThrowingKnifeComponent)
from components.burnable import ItemBurnable


class HealthPotion(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(x, y, '!', COLORS['violet'], 'Potion of Health',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      item=HealthPotionComponent())


class MagicMissileScroll(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Magic Missile',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      item=MagicMissileComponent(),
                      burnable=ItemBurnable())


class FireblastScroll(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Fireblast',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      item=FireblastComponent(),
                      burnable=ItemBurnable())


class ThrowingKnife(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(x, y, chr(24), COLORS['white'], 'Throwing Knife',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      item=ThrowingKnifeComponent())


ITEM_GROUPS = {
    ItemGroups.NONE: [],
    ItemGroups.ONE_HEALTH_POTION: [HealthPotion],
    ItemGroups.TWO_HEALTH_POTIONS: [HealthPotion]*2,
    ItemGroups.MAGIC_MISSILE_SCROLL: [MagicMissileScroll]*2,
    ItemGroups.FIREBLAST_SCROLL: [FireblastScroll],
    ItemGroups.THROWING_KNIFE: [ThrowingKnife],
}

ITEM_SCHEDULE = [
    (0.6, ItemGroups.NONE),
    (0.4*0.0, ItemGroups.ONE_HEALTH_POTION),
    (0.4*0.0, ItemGroups.TWO_HEALTH_POTIONS),
    (0.4*1.0, ItemGroups.MAGIC_MISSILE_SCROLL),
    (0.4*0.0, ItemGroups.FIREBLAST_SCROLL),
    (0.4*0.0, ItemGroups.THROWING_KNIFE)
]
