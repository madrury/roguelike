from etc.enum import ResultTypes, Elements

class LinearTransformer:
    """Base for classes that transform damage linearly.

    Attributes
    ----------
    elements: List[Element]
      The elements whose damage to reduce.

    addend: int
      The constant term in the linear transformation.

    multiplyer: int
      The multiplyer in the linear transformation.
    """
    def __init__(self, *, elements=None, addend=0, multiplyer=1):
        self.addend = addend
        self.multiplyer = multiplyer
        if elements is None:
            elements = []
        self.elements = set(elements)


class OffensiveLinearTransformer(LinearTransformer):
    """Modify a base amount of dealt damage with a linear transformation, and
    optionally add some elemental effect to the damage.
    """
    def transform(self, target, source, amount, *, elements=None):
        if elements == None:
            elements = {Elements.NONE}
        elements = self.elements.union(elements) 
        damage = self.multiplyer * amount + self.addend
        return [{
            ResultTypes.HARM: (
                target, source, damage, self.elements)}]


class DefensiveLinearTransformer(LinearTransformer):
    """Modify some base amount of recieved damage from a given collection of
    elements with a linear transformation.
    """
    def transform(self, target, source, amount, *, elements=None):
        if elements == None:
            elements = {Elements.NONE}
        print("Defensive Transformer: ", self.elements, target.name, source.name, amount, elements)
        damage = self.multiplyer * amount - self.addend
        if self.elements.intersection(elements):
            return [{
                ResultTypes.HARM: (
                    target, source, damage, list(elements))}]
        else:
            return [{
                ResultTypes.HARM: (
                    target, source, amount, list(elements))}]


