from etc.enum import ResultTypes


class Rechargeable:

    def __init__(self, charges_needed=100):
        self.charges = 0
        self.charges_needed = charges_needed

    def tick(self):
        self.charges += 1
        if self.charges >= self.charges_needed:
            self.charges = 0
            return [{
                ResultTypes.RECHARGE_ITEM: self.owner}]
        return []
