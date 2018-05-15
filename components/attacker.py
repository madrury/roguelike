from messages import Message
from etc.enum import ResultTypes, Elements

class Attacker:

    def __init__(self, power):
        self.power = power

    def attack(self, target):
        results = []
        if target.harmable is None:
            message = Message('{0} attacks {1}, but it does nothing.'.format(
                self.owner.name.capitalize(), target.name))
            results.append({ResultTypes.MESSAGE: message})
            return results
        damage = self.power - target.harmable.defense
        if damage > 0:
            attack_message = Message('{0} attacks {1} for {2} HP.'.format(
                self.owner.name.capitalize(), target.name, damage))
            results.append({ResultTypes.MESSAGE: attack_message})
            results.append({ResultTypes.DAMAGE: (target, self.owner, damage, [Elements.NONE])})
        else:
            attack_message = Message('{0} attacks {1}, but does no damage.'.format(
                self.owner.name.capitalize(), target.name))
            results.append({ResultTypes.MESSAGE: attack_message})
        return results
