from entity import Entity

from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups, Elements
from components.equipable import ArmorEquipable
from components.damage_transformers.defensive_transformers import (
    ElementalTransformer)


class LeatherArmor:

    @staticmethod
    def make(x, y, modifier=0):
        base_defense = 2
        name = 'Leather Armor ' + f'(+{modifier})'
        damage_transformer = ElementalTransformer(
            base_defense + modifier, Elements.NONE)
        return Entity(x, y, '&', COLORS['violet'], name,
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      equipable=ArmorEquipable(damage_transformer=[
                          damage_transformer]))
