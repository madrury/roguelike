from entity import Entity
from etc.colors import COLORS
from etc.chars import CHARS
from etc.enum import EntityTypes, RenderOrder, Elements

from components.commitable import BaseCommitable
from components.equipable import WeaponEquipable
from components.floatable import Floatable
from components.movable import Movable
from components.stats import WeaponStats

from components.callbacks.target_callbacks import (
    LanceCallback, AxeCallback)
from components.transformers.damage_transformers import OffensiveLinearTransformer


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
            equipable=WeaponEquipable(
                damage_transformers=[damage_transformer],
                target_callback=LanceCallback()),
            floatable=Floatable(),
            movable=Movable(),
            stats=WeaponStats(
                elements=elements,
                power=weapon_power,
                modifier=modifier))


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
            floatable=Floatable(),
            movable=Movable(),
            equipable=WeaponEquipable(
                damage_transformers=[damage_transformer],
                target_callback=AxeCallback()),
            stats=WeaponStats(
                elements=elements,
                power=weapon_power,
                modifier=modifier))
