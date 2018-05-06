from etc.enum import ResultTypes, Elements

class Swimmable:

    def __init__(self, stamina):
        self.max_stamina = stamina
        self.stamina = stamina

    def swim(self):
        results = []
        if self.stamina > 0:
            results.append({ResultTypes.CHANGE_SWIM_STAMINA: (self.owner, -1)})
        if self.stamina <= 0:
            results.append({ResultTypes.DAMAGE: (self.owner, 5, Elements.WATER)})
        return results

    def rest(self):
        results = []
        results.append({ResultTypes.CHANGE_SWIM_STAMINA: (self.owner, 1)})
        return results

    def change_stamina(self, change):
        if self.stamina < 0:
            self.stamina = 0
        else:
            self.stamina = min(max(0, self.stamina + change), self.max_stamina)
