from entity import Entity
from etc.colors import COLORS
from etc.chars import CHARS
from etc.enum import EntityTypes, RenderOrder, Elements

from components.commitable import BaseCommitable
from components.consumable import FinitelyConsumable
from components.equipable import WeaponEquipable
from components.floatable import Floatable
from components.movable import Movable
from components.stats import WeaponStats
from components.throwable import WeaponThrowable

from components.callbacks.target_callbacks import (
    LanceCallback, AxeCallback, SwordCallback)
from components.callbacks.move_callbacks import RaipierCallback
from components.transformers.damage_transformers import (
    OffensiveLinearTransformer)


class Lance:

    @staticmethod
    def make(x, y, *, modifier=0, elements=None):
        if not elements:
            elements = [Elements.NONE]
        weapon_power = 2 + modifier
        damage_transformer = OffensiveLinearTransformer(
            multiplyer=weapon_power,
            elements=elements)
        name = 'Lance ' + f'(+{modifier})'
        return Entity(x, y, CHARS['weapon'] , COLORS['violet'], name,
            entity_type=EntityTypes.ITEM,
            render_order=RenderOrder.ITEM,
            commitable=BaseCommitable(),
            consumable=FinitelyConsumable(uses=1),
            equipable=WeaponEquipable(
                damage_transformers=[damage_transformer],
                target_callback=LanceCallback()),
            floatable=Floatable(),
            movable=Movable(),
            stats=WeaponStats(
                elements=elements,
                power=weapon_power,
                modifier=modifier),
            throwable=WeaponThrowable())

class Sword:

    @staticmethod
    def make(x, y, *, modifier=0, elements=None):
        if not elements:
            elements = [Elements.NONE]
        weapon_power = 2 + modifier
        damage_transformer = OffensiveLinearTransformer(
            multiplyer=weapon_power,
            elements=elements)
        name = 'Sword ' + f'(+{modifier})'
        return Entity(x, y, CHARS['weapon'] , COLORS['violet'], name,
            entity_type=EntityTypes.ITEM,
            render_order=RenderOrder.ITEM,
            commitable=BaseCommitable(),
            consumable=FinitelyConsumable(uses=1),
            equipable=WeaponEquipable(
                damage_transformers=[damage_transformer],
                target_callback=SwordCallback()),
            floatable=Floatable(),
            movable=Movable(),
            stats=WeaponStats(
                elements=elements,
                power=weapon_power,
                modifier=modifier),
            throwable=WeaponThrowable())

class Axe:

    @staticmethod
    def make(x, y, *, modifier=0, elements=None):
        if not elements:
            elements = [Elements.NONE]
        weapon_power = 2 + modifier
        damage_transformer = OffensiveLinearTransformer(
            multiplyer=weapon_power)
        name = 'Axe ' + f'(+{modifier})'
        return Entity(x, y, CHARS['weapon'], COLORS['violet'], name,
            entity_type=EntityTypes.ITEM,
            render_order=RenderOrder.ITEM,
            commitable=BaseCommitable(),
            consumable=FinitelyConsumable(uses=1),
            floatable=Floatable(),
            movable=Movable(),
            equipable=WeaponEquipable(
                damage_transformers=[damage_transformer],
                target_callback=AxeCallback()),
            stats=WeaponStats(
                elements=elements,
                power=weapon_power,
                modifier=modifier),
            throwable=WeaponThrowable())

class Raipier:

    @staticmethod
    def make(x, y, *, modifier=0, elements=None):
        if not elements:
            elements = [Elements.NONE]
        weapon_power = 1 + modifier
        damage_transformer = OffensiveLinearTransformer(
            multiplyer=weapon_power)
        name = 'Raipier ' + f'(+{modifier})'
        return Entity(x, y, CHARS['weapon'], COLORS['violet'], name,
            entity_type=EntityTypes.ITEM,
            render_order=RenderOrder.ITEM,
            commitable=BaseCommitable(),
            consumable=FinitelyConsumable(uses=1),
            floatable=Floatable(),
            movable=Movable(),
            equipable=WeaponEquipable(
                damage_transformers=[damage_transformer],
                move_callback=RaipierCallback()),
            stats=WeaponStats(
                elements=elements,
                power=weapon_power,
                modifier=modifier),
            throwable=WeaponThrowable())
