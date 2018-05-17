from itertools import product

from messages import Message
from etc.enum import ResultTypes, Elements

class Attacker:

    def __init__(self, power, *,
                 damage_transformers=None,
                 target_callback=None):
        self.power = power
        self.damage_transformers = []
        self.target_callback = target_callback
        if damage_transformers:
            for transformer in damage_transformers:
                self.damage_transformers.append(transformer)

    def attack(self, game_map, target):
        results = []
        if target.harmable is None:
            message = Message(
                f'{self.owner} attacks {target.name}, but it does nothing.')
            results.append({ResultTypes.MESSAGE: message})
            return results
        # Collect list of targets.
        if self.target_callback:
            targets = self.target_callback.execute(
                game_map, target, self.owner)
        else:
            targets = [target]
        # Base damage is the attacker's power.
        damage = self.power
        # Do base damage to all targets.
        for target in targets:
            message = Message(f"{self.owner.name} attacks {target.name} "
                               "and does {damage} damage")
            results.append({
                ResultTypes.DAMAGE: (target, self.owner, damage, [Elements.NONE]),
                ResultTypes.MESSAGE: message})
        # Do transformed damage to all targets.
        for transformer, target in product(self.damage_transformers, targets):
            results.extend(transformer.transform_damage(target, self.owner, damage))
        return results

    def add_damage_transformers(self, transformers):
        for transformer in transformers:
            self.damage_transformers.append(transformer)

    def remove_damage_transformers(self, transformers):
        for transformer in transformers:
            self.damage_transformers.remove(transformer)
