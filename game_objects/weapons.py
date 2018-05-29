from entity import Entity
from etc.colors import COLORS
from etc.chars import CHARS
from etc.enum import EntityTypes, RenderOrder

from components.commitable import BaseCommitable
from components.equipable import WeaponEquipable
from components.floatable import Floatable

from components.callbacks.target_callbacks import (
    LanceCallback, AxeCallback)


class Lance:

    @staticmethod
    def make(x, y, modifier=0):
        base_offense = 3
        name = 'Lance ' + f'(+{modifier})'
        return Entity(x, y, CHARS['weapon'] , COLORS['violet'], name,
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      floatable=Floatable(),
                      movable=Movable(),
                      equipable=WeaponEquipable(
                          #damage_transformers=[damage_transformer],
                          target_callback=LanceCallback()))


class Axe:

    @staticmethod
    def make(x, y, modifier=0):
        base_offense = 2
        name = 'Axe ' + f'(+{modifier})'
        return Entity(x, y, CHARS['weapon'], COLORS['violet'], name,
                      entity_type=EntityTypes.ITEM,
                      render_order=RenderOrder.ITEM,
                      commitable=BaseCommitable(),
                      floatable=Floatable(),
                      movable=Movable(),
                      equipable=WeaponEquipable(
                          target_callback=AxeCallback()))
