from etc.enum import ResultTypes


class Consumable:

    def __init__(self, *, uses=5):
        self.uses = uses

    def consume(self):
        if self.uses <= 0:
            raise RuntimeError("Cannot consume {self.owner.name}, has zero "
                               "uses.")
        self.uses -=1
        if self.uses == 0:
            return [{ResultTypes.ITEM_CONSUMED: (True, self.owner)}]
        else:
            return []
