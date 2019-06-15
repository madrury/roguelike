from entity import Entity

from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, Elements

from components.commitable import BaseCommitable
from components.equipable import ArmorEquipable
from components.floatable import Floatable
from components.movable import Movable
from components.stats import ArmorStats
from components.transformers.damage_transformers import (
    DefensiveLinearTransformer)

from components.callbacks.damage_callbacks import ReflectCallback


class LeatherArmor:

    @staticmethod
    def make(x, y, modifier=0, elements=None):
        if not elements:
            elements=[Elements.NONE]
        name = 'Leather Armor ' + f'(+{modifier})'
        base_defense = 2
        damage_modifier = base_defense + modifier
        damage_transformer = DefensiveLinearTransformer(
             elements=elements,
             addend=damage_modifier)
        return Entity(x, y, '&', COLORS['violet'], name,
            entity_type=EntityTypes.ITEM,
            render_order=RenderOrder.ITEM,
            commitable=BaseCommitable(),
            floatable=Floatable(),
            movable=Movable(),
            equipable=ArmorEquipable(damage_transformers=[
                damage_transformer]),
            stats=ArmorStats(
                defense=base_defense,
                modifier=modifier,
                elements=elements))


class ReflectSuit:

    @staticmethod
    def make(x, y, modifier=0, elements=None):
        if not elements:
            elements=[Elements.NONE]
        name = 'Ninja Suit' + f'(+{modifier})'
        damage_callback = ReflectCallback()
        base_defense = 1
        damage_modifier = base_defense + modifier
        damage_transformer = DefensiveLinearTransformer(
             elements=elements,
             addend=damage_modifier)
        return Entity(x, y, '&', COLORS['violet'], name,
            entity_type=EntityTypes.ITEM,
            render_order=RenderOrder.ITEM,
            commitable=BaseCommitable(),
            floatable=Floatable(),
            movable=Movable(),
            equipable=ArmorEquipable(
                damage_callbacks=[damage_callback]),
            stats=ArmorStats(
                defense=base_defense,
                modifier=modifier,
                elements=elements))
