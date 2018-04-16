from entity import Entity

from spawnable.spawnable import Spawnable
from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups
from components.item import HealthPotionComponent, MagicMissileComponent


class HealthPotion(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(x, y, '!', COLORS['violet'], 'Health Potion',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      item=HealthPotionComponent())


class MagicMissileScroll(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(x, y, '%', COLORS['violet'], 'Magic Missile Scroll',
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      item=MagicMissileComponent())


ITEM_GROUPS = {
    ItemGroups.NONE: [],
    ItemGroups.ONE_HEALTH_POTION: [HealthPotion],
    ItemGroups.TWO_HEALTH_POTIONS: [HealthPotion]*2,
    ItemGroups.MAGIC_MISSILE_SCROLL: [MagicMissileScroll],
}

ITEM_SCHEDULE = [
    (0.6, ItemGroups.NONE),
    (0.4*0.6, ItemGroups.ONE_HEALTH_POTION),
    (0.4*0.1, ItemGroups.TWO_HEALTH_POTIONS),
    (0.4*0.3, ItemGroups.MAGIC_MISSILE_SCROLL)
]
