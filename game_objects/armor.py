from entity import Entity

from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups, Elements

from components.commitable import BaseCommitable
from components.equipable import ArmorEquipable
from components.damage_transformers.defensive_transformers import (
    ElementalTransformer)
from components.callbacks.damage_callbacks import ReflectCallback


class LeatherArmor:

    @staticmethod
    def make(x, y, modifier=0):
        base_defense = 2
        name = 'Leather Armor ' + f'(+{modifier})'
        damage_transformer = ElementalTransformer(
            base_defense + modifier, [Elements.NONE])
        return Entity(x, y, '&', COLORS['violet'], name,
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      equipable=ArmorEquipable(damage_transformers=[
                          damage_transformer]))


class LeatherArmorOfFireResist:
    @staticmethod
    def make(x, y, modifier=0):
        base_defense = 2
        name = 'Leather Armor of Fire Resist' + f'(+{modifier})'
        damage_transformer = ElementalTransformer(
            base_defense + modifier, [Elements.NONE, Elements.FIRE])
        return Entity(x, y, '&', COLORS['violet'], name,
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      equipable=ArmorEquipable(damage_transformers=[damage_transformer]))

class ReflectSuit:

    @staticmethod
    def make(x, y, modifier=0):
        base_defense = 1
        name = 'Ninja Suit' + f'(+{modifier})'
        damage_callback = ReflectCallback()
        return Entity(x, y, '&', COLORS['violet'], name,
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      equipable=ArmorEquipable(damage_callbacks=[damage_callback]))
