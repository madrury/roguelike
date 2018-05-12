from entity import Entity

from etc.colors import COLORS
from etc.enum import EntityTypes, RenderOrder, ItemGroups, Elements
from components.equipable import ArmorEquipable
from components.damage_filters.defensive_filters import ElementalFilter


class LeatherArmor:

    @staticmethod
    def make(x, y, modifier=0):
        base_defense = 2
        name = 'Leather Armor ' + f'(+{modifier})'
        return Entity(x, y, '&', COLORS['violet'], name,
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      equipable=ArmorEquipable(damage_filters=[
                            ElementalFilter(base_defense + modifier, Elements.NONE)]))
