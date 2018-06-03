from etc.enum import ResultTypes
from etc.colors import COLORS
from messages import Message


class BaseEquipable:
    """Just provide an default display in the inventory indicating whether the
    item is equipped or not.
    """
    def make_menu_display(self):
        return ["", "(E)"][int(self.equipped)]


class ArmorEquipable(BaseEquipable):
    """Equippable armor.

    The behaviour of armor is govened by a list of damage_transformers and
    damage_callbacks.  When armors is equipped, these are copied into
    corresponding slots on the entities harmable component.
    """
    def __init__(self, *, damage_transformers=None, damage_callbacks=None):
        self.equipped = False
        self.damage_transformers = []
        self.damage_callbacks = []
        if damage_transformers:
            for transformer in damage_transformers:
                self.damage_transformers.append(transformer)
        if damage_callbacks:
            for callback in damage_callbacks:
                self.damage_callbacks.append(callback)

    def equip(self, entity):
        results = []
        results.append({
            ResultTypes.EQUIP_ARMOR: (entity, self.owner)})
        return results

    def remove(self, entity):
        results = []
        results.append({
            ResultTypes.REMOVE_ARMOR: (entity, self.owner)})
        return results


class WeaponEquipable(BaseEquipable):
    """Equippable armor.

    The behaviour of a weapon is govened by a list of damage_transformers and a
    target_callback.  When a weapon is equipped, these are copied into
    corresponding slots on the entities attacker component.
    """
    def __init__(self, *, damage_transformers=None,
                          target_callback=None,
                          move_callback=None):
        self.equipped = False
        self.damage_transformers = []
        self.target_callback = target_callback
        self.move_callback = move_callback
        if damage_transformers:
            for transformer in damage_transformers:
                self.damage_transformers.append(transformer)

    def equip(self, entity):
        results = []
        results.append({
            ResultTypes.EQUIP_WEAPON: (entity, self.owner)})
        return results

    def remove(self, entity):
        results = []
        results.append({
            ResultTypes.REMOVE_WEAPON: (entity, self.owner)})
        return results
