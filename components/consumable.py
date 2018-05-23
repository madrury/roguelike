from etc.enum import ResultTypes


class Consumable:

    def __init__(self, *, uses=1):
        self.uses = uses

    def consume(self):
        if self.uses <= 0:
            raise RuntimeError("Cannot consume {self.owner.name}, has zero "
                               "uses.")
        self.uses -=1
        if self.uses == 0:
            print("Item consumed")
            return [{
                ResultTypes.ITEM_CONSUMED: (True, self.owner),
                ResultTypes.END_TURN: True}]
        else:
            return [{
                ResultTypes.END_TURN: True}]
