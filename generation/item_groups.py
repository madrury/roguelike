from enum import Enum, auto

from game_objects.items import (
    HealthPotion, PowerPotion, MagicMissileScroll, FireblastScroll,
    WaterblastScroll, ThrowingKnife, FireStaff)
from game_objects.armor import (
    LeatherArmor, ReflectSuit)
from game_objects.weapons import Lance, Axe, Sword


class ItemGroups(Enum):
    NONE = auto()
    ONE_HEALTH_POTION = auto()
    POWER_POTION = auto()
    TWO_HEALTH_POTIONS = auto()
    MAGIC_MISSILE_SCROLL = auto()
    FIREBLAST_SCROLL = auto()
    WATERBLAST_SCROLL = auto()
    THROWING_KNIFE = auto()
    FIRE_STAFF = auto()
    LANCE = auto()
    SWORD = auto()
    AXE = auto()
    LEATHER_ARMOR = auto()
    LEATHER_ARMOR_OF_FIRE_RESIST = auto()
    REFLECT_SUIT = auto()


ITEM_GROUPS = {
    ItemGroups.NONE: [],
    ItemGroups.ONE_HEALTH_POTION: [HealthPotion],
    ItemGroups.TWO_HEALTH_POTIONS: [HealthPotion]*2,
    ItemGroups.POWER_POTION: [PowerPotion],
    ItemGroups.MAGIC_MISSILE_SCROLL: [MagicMissileScroll],
    ItemGroups.FIREBLAST_SCROLL: [FireblastScroll],
    ItemGroups.WATERBLAST_SCROLL: [WaterblastScroll],
    ItemGroups.THROWING_KNIFE: [ThrowingKnife],
    ItemGroups.FIRE_STAFF: [FireStaff],
    ItemGroups.LANCE: [Lance],
    ItemGroups.SWORD: [Sword],
    ItemGroups.AXE: [Axe],
    ItemGroups.LEATHER_ARMOR: [LeatherArmor],
    ItemGroups.REFLECT_SUIT: [ReflectSuit],
}

ITEM_SCHEDULES = [
    [
        (0.5, ItemGroups.NONE),
        (1.0*0.3, ItemGroups.ONE_HEALTH_POTION),
        (1.0*0.1, ItemGroups.POWER_POTION),
        (1.0*0.0, ItemGroups.TWO_HEALTH_POTIONS),
        (1.0*0.0, ItemGroups.MAGIC_MISSILE_SCROLL),
        (1.0*0.0, ItemGroups.FIREBLAST_SCROLL),
        (1.0*0.0, ItemGroups.WATERBLAST_SCROLL),
        (1.0*0.1, ItemGroups.THROWING_KNIFE),
        (1.0*0.0, ItemGroups.FIRE_STAFF),
        (1.0*0.0, ItemGroups.LANCE),
        (1.0*0.0, ItemGroups.SWORD),
        (1.0*0.0, ItemGroups.AXE),
        (1.0*0.0, ItemGroups.LEATHER_ARMOR),
        (1.0*0.0, ItemGroups.REFLECT_SUIT)],
    [
        (0.5, ItemGroups.NONE),
        (1.0*0.2, ItemGroups.ONE_HEALTH_POTION),
        (1.0*0.1, ItemGroups.POWER_POTION),
        (1.0*0.0, ItemGroups.TWO_HEALTH_POTIONS),
        (1.0*0.05, ItemGroups.MAGIC_MISSILE_SCROLL),
        (1.0*0.05, ItemGroups.FIREBLAST_SCROLL),
        (1.0*0.0, ItemGroups.WATERBLAST_SCROLL),
        (1.0*0.1, ItemGroups.THROWING_KNIFE),
        (1.0*0.0, ItemGroups.FIRE_STAFF),
        (1.0*0.0, ItemGroups.LANCE),
        (1.0*0.0, ItemGroups.SWORD),
        (1.0*0.0, ItemGroups.AXE),
        (1.0*0.0, ItemGroups.LEATHER_ARMOR),
        (1.0*0.0, ItemGroups.REFLECT_SUIT)],
    [
        (0.4, ItemGroups.NONE),
        (1.0*0.1, ItemGroups.ONE_HEALTH_POTION),
        (1.0*0.1, ItemGroups.POWER_POTION),
        (1.0*0.0, ItemGroups.TWO_HEALTH_POTIONS),
        (1.0*0.05, ItemGroups.MAGIC_MISSILE_SCROLL),
        (1.0*0.05, ItemGroups.FIREBLAST_SCROLL),
        (1.0*0.05, ItemGroups.WATERBLAST_SCROLL),
        (1.0*0.1, ItemGroups.THROWING_KNIFE),
        (1.0*0.05, ItemGroups.FIRE_STAFF),
        (1.0*0.0, ItemGroups.LANCE),
        (1.0*0.0, ItemGroups.SWORD),
        (1.0*0.1, ItemGroups.AXE),
        (1.0*0.0, ItemGroups.LEATHER_ARMOR),
        (1.0*0.0, ItemGroups.REFLECT_SUIT)],
]
