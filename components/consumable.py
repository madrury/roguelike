from etc.enum import ResultTypes


class FinitelyConsumable:
    """Track the number of times an item has been used.

    This component is used on items that can only be consumed a finite number
    of times.  It internally tracks a counter of remaining uses, and signals
    for the item to be destroyed when fully consumed.

    Parameters
    ----------
    uses: int
      The number of time the item can be used.

    discard_on_empty: bool
      Should the item be discarded when the remaining uses drops to zero?

    display_on_one:
      Should the remaining uses be displayed when there are one (or zero) uses?
    """
    def __init__(self, *, uses=1, discard_on_empty=True, display_on_one=False):
        self.uses = uses
        self.discard_on_empty = discard_on_empty
        self.display_on_one = display_on_one

    def consume(self):
        self.uses = max(0, self.uses - 1)
        if self.uses == 0:
            return [{
                ResultTypes.ITEM_CONSUMED: (self.discard_on_empty, self.owner),
                ResultTypes.END_TURN: True}]
        else:
            return [{
                ResultTypes.END_TURN: True}]

    def make_menu_display(self):
        if self.uses <= 1 and not self.display_on_one:
            return ""
        else:
            return f"[{self.uses}]"


class InfinitelyConsumable:
    """Component for items that can be used indefinately."""
    def consume(self):
        return []

    def make_menu_display(self):
        return ""
