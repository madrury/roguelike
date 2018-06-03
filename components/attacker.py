from itertools import product

from messages import Message
from etc.enum import ResultTypes, Elements

class Attacker:
    """Component for entites that can physically attack other entities.

    Attacks are based on an attack power status.  The baseline case, if the
    entity has nothing equipped, is an amount of non-elemental damage equal to
    the entities attack power status.

    If the entity has weapons equipped the damage_transformers and
    target_callback attributes come into play, which add special properties to
    the attack.

    damage_tranformers:
      Transform the base attack power damage, increasing or decreasing it, and
      adding elemental attributed.

    target_callback:
      Add additional targets to the attack. An axe, for example, targets all
      spaces adjacent to the player on any succesful attack.

    Finally, move_callback is used to support attacks that do not neccessarily
    target monsters only adjacent to the player.
    """
    def __init__(self, power, *,
                 damage_transformers=None,
                 target_callback=None,
                 move_callback=None):
        self.power = power
        self.damage_transformers = []
        self.target_callback = target_callback
        self.move_callback = move_callback
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
        # Collect list of targets of this attack.
        if self.target_callback:
            targets = self.target_callback.execute(
                game_map, target, self.owner)
        else:
            targets = [target]
        # Now compute the damage to deal.  There are two cases:
        # - If there are no damage transformers equipped, baseline
        # non-elemental damage is dealt equal to the attacker's power.
        #  - Otherwise, the equipped damage transformers are used to get the
        # final damage.
        damage = self.power
        if self.damage_transformers == []:
            results.append({
                ResultTypes.DAMAGE: (target, self.owner, damage, [Elements.NONE])})
        # No need for an else, this is an empty for loop if damage_transformers
        # is an empty list.
        for transformer, target in product(self.damage_transformers, targets):
            results.extend(
                transformer.transform(target, self.owner, damage))
        results.append({ResultTypes.END_TURN: True})
        return results

    def add_damage_transformers(self, transformers):
        for transformer in transformers:
            self.damage_transformers.append(transformer)

    def remove_damage_transformers(self, transformers):
        for transformer in transformers:
            self.damage_transformers.remove(transformer)
