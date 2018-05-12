class ArmorEquipable:

    def __init__(self, damage_transformers=None):
        self.damage_transformers = []
        if damage_transformers:
            for transformer in damage_transformers:
                self.damage_transformers.append(transformer)

    def equip(self, entity):
        if not hasattr(entity, "harmable"):
            raise AttributeError("Non harmable entities cannot equip Armor")
        for transformer in self.damage_transformers:
            entity.harmable.damage_transformers.append(transformer)

    def unequip(self, entity):
        for transformer in self.damage_transformers:
            entity.harmable.damage_transformers.remove(transformer)
