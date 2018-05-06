from messages import Message
from etc.enum import ResultTypes, Elements

class Harmable:

    def __init__(self, hp, defense, 
                 fire_modifier=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.fire_modifier = fire_modifier

    def take_damage(self, amount, element):
        if element == Elements.FIRE:
            amount -= self.fire_modifier
        self.hp -= amount
        results = []
        if self.hp <= 0:
            results.append({ResultTypes.DEAD_ENTITY: self.owner})
        return results


class NullHarmable:

    def take_damage(self, amount, element):
        return []
