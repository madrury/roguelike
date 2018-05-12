class ArmorEquipable:

    def __init__(self, damage_filters=None):
        self.damage_filters = []
        if damage_filters:
            for filter in damage_filters:
                self.damage_filters.append(filter)

    def equip(self, entity):
        if not hasattr(entity, "harmable"):
            raise AttributeError("Non harmable entities cannot equip Armor")
        for filter in self.damage_filters:
            entity.harmable.damage_filters.append(filter)

    def unequip(self, entity):
        for filter in self.damage_filters:
            entity.harmable.damage_filters.remove(filter)
