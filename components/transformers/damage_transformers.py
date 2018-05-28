class ElementalTransformer:
    """Reduce damage of a certain element by some amount.

    Attributes
    ----------
    strength: int
      The amount to reduce damage.

    element: Element
      The elements whose damage to reduce.
    """
    def __init__(self, elements, *, strength=0, multiplyer=1):
        self.strength = strength
        self.multiplyer = multiplyer
        self.elements = set(elements)

    def transform_damage(self, amount, elements):
        if self.elements.intersection(elements):
            return max(0, self.multiplyer * amount - self.strength)
        return amount
