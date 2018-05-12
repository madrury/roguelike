from etc.enum import ItemGroups
from entities.items import (
    HealthPotion, MagicMissileScroll, FireblastScroll, ThrowingKnife)


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
