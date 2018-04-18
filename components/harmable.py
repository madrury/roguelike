from game_messages import Message
from etc.enum import ResultTypes

class Harmable:

    def __init__(self, hp, defense):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense

    def take_damage(self, amount):
        results = []
        self.hp -= amount
        if self.hp <= 0:
            results.append({ResultTypes.DEAD_ENTITY: self.owner})
        return results
