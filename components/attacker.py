from game_messages import Message

class Attacker:

    def __init__(self, power):
        self.power = power

    def attack(self, target):
        results = []
        if target.harmable is None:
            message = Message('{0} attacks {1}, but it does nothing.'.format(
                self.owner.name.capitalize(), target.name))
            results.append({'message': message})
            return results
        damage = self.power - target.harmable.defense
        if damage > 0:
            attack_message = Message('{0} atacks {1} for {2} HP.'.format(
                self.owner.name.capitalize(), target.name, damage))
            results.append({'message': attack_message})
            results.append({'damage': (target, damage)})
        else:
            attack_message = Message('{0} atacks {1}, but does no damage.'.format(
                self.owner.name.capitalize(), target.name))
            results.append({'message': attack_message})
        return results
