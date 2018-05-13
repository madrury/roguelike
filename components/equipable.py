from etc.enum import ResultTypes
from etc.colors import COLORS
from messages import Message


class ArmorEquipable:

    def __init__(self, damage_transformers=None):
        self.equipped = False
        self.damage_transformers = []
        if damage_transformers:
            for transformer in damage_transformers:
                self.damage_transformers.append(transformer)

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
