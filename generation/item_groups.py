from etc.enum import ItemGroups
from game_objects.items import (
    HealthPotion, MagicMissileScroll, FireblastScroll, WaterblastScroll,
    ThrowingKnife)
from game_objects.armor import (
    LeatherArmor, ReflectSuit)
from game_objects.weapons import Lance, Axe


ITEM_GROUPS = {
    ItemGroups.NONE: [],
    ItemGroups.ONE_HEALTH_POTION: [HealthPotion],
    ItemGroups.TWO_HEALTH_POTIONS: [HealthPotion]*2,
    ItemGroups.MAGIC_MISSILE_SCROLL: [MagicMissileScroll]*2,
    ItemGroups.FIREBLAST_SCROLL: [FireblastScroll],
    ItemGroups.WATERBLAST_SCROLL: [WaterblastScroll],
    ItemGroups.THROWING_KNIFE: [ThrowingKnife],
    ItemGroups.LANCE: [Lance],
    ItemGroups.AXE: [Axe],
    ItemGroups.LEATHER_ARMOR: [LeatherArmor],
    ItemGroups.REFLECT_SUIT: [ReflectSuit],

}

ITEM_SCHEDULE = [
    (0.0, ItemGroups.NONE),
    (1.0*0.0, ItemGroups.ONE_HEALTH_POTION),
    (1.0*0.0, ItemGroups.TWO_HEALTH_POTIONS),
    (1.0*0.0, ItemGroups.MAGIC_MISSILE_SCROLL),
    (1.0*0.0, ItemGroups.FIREBLAST_SCROLL),
    (1.0*0.0, ItemGroups.WATERBLAST_SCROLL),
    (1.0*0.0, ItemGroups.THROWING_KNIFE),
    (1.0*0.25, ItemGroups.LANCE),
    (1.0*0.25, ItemGroups.AXE),
    (1.0*0.25, ItemGroups.LEATHER_ARMOR),
    (1.0*0.25, ItemGroups.REFLECT_SUIT),
]
