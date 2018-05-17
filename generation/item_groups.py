from etc.enum import ItemGroups
from game_objects.items import (
    HealthPotion, MagicMissileScroll, FireblastScroll, ThrowingKnife)
from game_objects.armor import (
    LeatherArmor, LeatherArmorOfFireResist, ReflectSuit)
from game_objects.weapons import Lance


ITEM_GROUPS = {
    ItemGroups.NONE: [],
    ItemGroups.ONE_HEALTH_POTION: [HealthPotion],
    ItemGroups.TWO_HEALTH_POTIONS: [HealthPotion]*2,
    ItemGroups.MAGIC_MISSILE_SCROLL: [MagicMissileScroll]*2,
    ItemGroups.FIREBLAST_SCROLL: [FireblastScroll],
    ItemGroups.THROWING_KNIFE: [ThrowingKnife],
    ItemGroups.LANCE: [Lance],
    ItemGroups.LEATHER_ARMOR: [LeatherArmor],
    ItemGroups.LEATHER_ARMOR_OF_FIRE_RESIST: [LeatherArmorOfFireResist],
    ItemGroups.REFLECT_SUIT: [ReflectSuit],

}

ITEM_SCHEDULE = [
    (0.6, ItemGroups.NONE),
    (0.4*0.0, ItemGroups.ONE_HEALTH_POTION),
    (0.4*0.0, ItemGroups.TWO_HEALTH_POTIONS),
    (0.4*0.0, ItemGroups.MAGIC_MISSILE_SCROLL),
    (0.4*0.0, ItemGroups.FIREBLAST_SCROLL),
    (0.4*0.0, ItemGroups.THROWING_KNIFE),
    (0.4*0.8, ItemGroups.LANCE),
    (0.4*0.0, ItemGroups.LEATHER_ARMOR),
    (0.4*0.1, ItemGroups.REFLECT_SUIT),
    (0.4*0.1, ItemGroups.LEATHER_ARMOR_OF_FIRE_RESIST)
]
