from etc.enum import ResultTypes
from etc.colors import COLORS
from messages import Message


class ArmorEquipable:

    def __init__(self, damage_transformers=None):
        self.damage_transformers = []
        if damage_transformers:
            for transformer in damage_transformers:
                self.damage_transformers.append(transformer)

    def equip(self, entity):
        results = []
        message = f"{entity.name} equipped {self.owner.name}"
        results.append({
            ResultTypes.MESSAGE: Message(message, COLORS['white']),
            ResultTypes.ADD_DAMAGE_TRANSFORMERS: (
                entity, self.damage_transformers)})
        return results

    def unequip(self, entity):
        results = []
        message = f"{entity.name} un-equipped {self.owner.name}"
        results.append({
            ResultTypes.MESSAGE: Message(message, COLORS['white']),
            ResultTypes.REMOVE_DAMAGE_TRANSFORMERS: (
                entity, self.damage_transformers)})
        return results
