from enum import Enum, auto

from game_objects.items import (
    HealthPotion, PowerPotion, SpeedPotion, ConfusionPotion, TeleportationPotion,
    MagicMissileScroll, FireblastScroll, WaterblastScroll,
    FireStaff, IceStaff,
    ThrowingKnife)
from game_objects.armor import LeatherArmor, ReflectSuit
from game_objects.weapons import Lance, Axe, Sword, Raipier

from generation.scheduler import CompositeScheduler


class ItemSpawnGroups(Enum):
    NONE = auto()
    # Potions
    HEALTH_POTION = auto()
    POWER_POTION = auto()
    SPEED_POTION = auto()
    CONFUSION_POTION = auto()
    TELEPORTATION_POTION = auto()
    # Scrolls
    MAGIC_MISSILE_SCROLL = auto()
    FIREBLAST_SCROLL = auto()
    WATERBLAST_SCROLL = auto()
    # Magic Staffs
    FIRE_STAFF = auto()
    ICE_STAFF = auto()
    # Weapons
    THROWING_KNIFE = auto()
    LANCE = auto()
    SWORD = auto()
    AXE = auto()
    RAIPIER = auto()
    # Armor
    LEATHER_ARMOR = auto()
    REFLECT_SUIT = auto()
    # TODO: Figure out how to spawn magic weapons.
    LEATHER_ARMOR_OF_FIRE_RESIST = auto()


ITEM_SPAWN_GROUPS = {
    ItemSpawnGroups.NONE: [],

    ItemSpawnGroups.HEALTH_POTION: [HealthPotion],
    ItemSpawnGroups.POWER_POTION: [PowerPotion],
    ItemSpawnGroups.SPEED_POTION: [SpeedPotion],
    ItemSpawnGroups.CONFUSION_POTION: [ConfusionPotion],
    ItemSpawnGroups.TELEPORTATION_POTION: [TeleportationPotion],

    ItemSpawnGroups.MAGIC_MISSILE_SCROLL: [MagicMissileScroll],
    ItemSpawnGroups.FIREBLAST_SCROLL: [FireblastScroll],
    ItemSpawnGroups.WATERBLAST_SCROLL: [WaterblastScroll],

    ItemSpawnGroups.FIRE_STAFF: [FireStaff],
    ItemSpawnGroups.ICE_STAFF: [IceStaff],

    ItemSpawnGroups.THROWING_KNIFE: [ThrowingKnife],
    ItemSpawnGroups.LANCE: [Lance],
    ItemSpawnGroups.SWORD: [Sword],
    ItemSpawnGroups.AXE: [Axe],
    ItemSpawnGroups.RAIPIER: [Raipier],

    ItemSpawnGroups.LEATHER_ARMOR: [LeatherArmor],
    ItemSpawnGroups.REFLECT_SUIT: [ReflectSuit]
}


class ItemSchedule(CompositeScheduler):
    default_group = ItemSpawnGroups.NONE


class ItemSpawnSchedules(Enum):
    NONE = auto()
    # Atomic spawn groups
    BASIC_POTIONS = auto()
    INTERMEDIATE_POTIONS = auto()
    MAGIC_MISSILE_SCROLL = auto()
    AREA_OF_EFFECT_SCROLLS = auto()
    MAGIC_STAFFS = auto()
    THROWING_KNIFES = auto()
    BASIC_WEAPONS = auto()
    BASIC_ARMOR = auto()


# Define the atomic spawn groups
ITEM_SPAWN_SCHEDULES = {
    ItemSpawnSchedules.NONE: ItemSchedule(),
    ItemSpawnSchedules.BASIC_POTIONS: ItemSchedule({
        ItemSpawnGroups.NONE: 0.8,
        ItemSpawnGroups.HEALTH_POTION: 0.15,
        ItemSpawnGroups.POWER_POTION: 0.05
    }),
    ItemSpawnSchedules.INTERMEDIATE_POTIONS: ItemSchedule({
        ItemSpawnGroups.NONE: 0.85,
        ItemSpawnGroups.SPEED_POTION: 0.05,
        ItemSpawnGroups.TELEPORTATION_POTION: 0.05,
        ItemSpawnGroups.CONFUSION_POTION: 0.05
    }),
    ItemSpawnSchedules.MAGIC_MISSILE_SCROLL: ItemSchedule({
        ItemSpawnGroups.NONE: 0.95,
        ItemSpawnGroups.MAGIC_MISSILE_SCROLL: 0.05
    }),
    ItemSpawnSchedules.AREA_OF_EFFECT_SCROLLS: ItemSchedule({
        ItemSpawnGroups.NONE: 0.9,
        ItemSpawnGroups.FIREBLAST_SCROLL: 0.05,
        ItemSpawnGroups.WATERBLAST_SCROLL: 0.05,
    }),
    ItemSpawnSchedules.MAGIC_STAFFS: ItemSchedule({
        ItemSpawnGroups.NONE: 0.9,
        ItemSpawnGroups.FIRE_STAFF: 0.05,
        ItemSpawnGroups.ICE_STAFF: 0.05
    }),
    ItemSpawnSchedules.THROWING_KNIFES: ItemSchedule({
        ItemSpawnGroups.NONE: 0.95,
        ItemSpawnGroups.THROWING_KNIFE: 0.05
    }),
    ItemSpawnSchedules.BASIC_WEAPONS: ItemSchedule({
        ItemSpawnGroups.NONE: 0.8,
        ItemSpawnGroups.SWORD: 0.05,
        ItemSpawnGroups.LANCE: 0.05,
        ItemSpawnGroups.AXE: 0.05,
        ItemSpawnGroups.RAIPIER: 0.05
    }),
    ItemSpawnSchedules.BASIC_ARMOR: ItemSchedule({
        ItemSpawnGroups.NONE: 0.9,
        ItemSpawnGroups.LEATHER_ARMOR: 0.1
    })
}