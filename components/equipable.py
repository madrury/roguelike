from etc.enum import ResultTypes
from etc.colors import COLORS
from messages import Message


class ArmorEquipable:
    """Equippable armor.

    The behaviour of armor is govened by a list od damage_transformers.  These
    object has a transform_damage method which is used (in the case of armor)
    to reduce or nullify damage.
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
