from enum import Enum, auto

from entity import Entity, EntityTypes
from render_functions import RenderOrder

from spawnable.spawnable import Spawnable
from etc.colors import COLORS
from components.item import HealthPotionComponent, MagicMissileComponent


class ItemGroups(Enum):
    NONE = auto()
    ONE_HEALTH_POTION = auto()
    TWO_HEALTH_POTIONS = auto()
    MAGIC_MISSILE_SCROLL = auto()


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
    (0.5, ItemGroups.NONE),
    (0.5*0.5, ItemGroups.ONE_HEALTH_POTION),
    (0.5*0.1, ItemGroups.TWO_HEALTH_POTIONS),
    (0.5*0.4, ItemGroups.MAGIC_MISSILE_SCROLL)
]
