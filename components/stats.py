class WeaponStats:

    def __init__(self, *,
                 power=None,
                 modifier=None,
                 elements=None):
        self.power = power
        self.modifier = modifier
        elements=elements


class ArmorStats:

    def __init__(self, *,
                 defense=None,
                 modifier=None,
                 elements=None):
        self.defense = defense
        modifier=modifier
        self.elements = elements
