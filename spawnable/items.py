from enum import Enum, auto

from entity import Entity
from render_functions import RenderOrder

from spawnable.spawnable import Spawnable
from etc.colors import COLORS
from components.item import HealthPotionComponent


class ItemGroups(Enum):
    NONE = auto()
    ONE_HEALTH_POTION = auto()
    TWO_HEALTH_POTIONS = auto()


class HealthPotion(Spawnable):

    @staticmethod
    def make(x, y):
        return Entity(x, y, '!', COLORS['violet'], 'Health Potion',
                     render_order=RenderOrder.ITEM,
                     item=HealthPotionComponent())


ITEM_GROUPS = {
    ItemGroups.NONE: [],
    ItemGroups.ONE_HEALTH_POTION: [HealthPotion],
    ItemGroups.TWO_HEALTH_POTIONS: [HealthPotion]*2
}

ITEM_SCHEDULE = [
    (0.5, ItemGroups.NONE),
    (0.5*0.75, ItemGroups.ONE_HEALTH_POTION),
    (0.5*0.25, ItemGroups.TWO_HEALTH_POTIONS)
]
