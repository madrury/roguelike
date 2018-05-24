from etc.enum import ResultTypes


class FinitelyConsumable:
    """Track the number of times an item has been used.

    This component is used on items that can only be consumed a finite number
    of times.  It internally tracks a counter of remaining uses, and signals
    for the item to be destroyed when fully consumed.
    """
    def __init__(self, *, uses=1):
        self.uses = uses

    def consume(self):
        if self.uses <= 0:
            raise RuntimeError("Cannot consume {self.owner.name}, has zero "
                               "uses.")
        self.uses -=1
        if self.uses == 0:
            return [{
                ResultTypes.ITEM_CONSUMED: (True, self.owner),
                ResultTypes.END_TURN: True}]
        else:
            return [{
                ResultTypes.END_TURN: True}]

    def make_menu_display(self):
        return f"[{self.uses}]"


class InfinitelyConsumable:
    """Component for items that can be used indefinately."""
    def consume(self):
        return []

    def make_menu_display(self):
        return ""
