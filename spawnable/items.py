from entity import Entity

from spawnable.spawnable import Spawnable
from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups
from components.item import (
    HealthPotionComponent, MagicMissileComponent,
    FireblastComponent, ThrowingKnifeComponent)


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
                      item=MagicMissileComponent())


class FireblastScroll(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Scroll of Fireblast',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      item=FireblastComponent())


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
    ItemGroups.MAGIC_MISSILE_SCROLL: [MagicMissileScroll],
    ItemGroups.FIREBLAST_SCROLL: [MagicMissileScroll],
}

ITEM_SCHEDULE = [
    (0.6, ItemGroups.NONE),
    (0.4*0.6, ItemGroups.ONE_HEALTH_POTION),
    (0.4*0.1, ItemGroups.TWO_HEALTH_POTIONS),
    (0.4*0.2, ItemGroups.MAGIC_MISSILE_SCROLL),
    (0.4*0.1, ItemGroups.FIREBLAST_SCROLL)
]
