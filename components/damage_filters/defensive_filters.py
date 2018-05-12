class ElementalFilter:

    def __init__(self, strength, element):
        self.strength = strength
        self.element = element

    def filter_damage(self, amount, element):
        if element == self.element:
            return max(0, amount - self.strength)
        return amount

