from game_messages import Message
from etc.colors import COLORS
from etc.enum import EntityTypes, ItemTargeting


class HealthPotionComponent:
    """A health component.

    Used on the player themselves, this heals some amount of HP.
    """
    def __init__(self, healing=5):
        self.name = "healing potion"
        self.targeting = ItemTargeting.PLAYER
        self.healing = healing

    def use(self, player):
        results = []
        if player.harmable.hp == player.harmable.max_hp:
            message = Message('You are already at full health.', 
                              COLORS.get('white'))
            results.append({'item_consumed': (False, self.owner), 
                            'message': message})
        else:
            message = Message('You wounds start to heal.', 
                              COLORS.get('green'))
            results.append({'item_consumed': (True, self.owner),
                            'heal': (player, self.healing),
                            'message': message})
        return results


class MagicMissileComponent:
    """A Magic Missile spell.

    This targets the closest enemy, and deals an amount of damage.
    """
    def __init__(self, damage=6, spell_range=10):
        self.name = "magic missile"
        self.targeting = ItemTargeting.CLOSEST_MONSTER
        self.damage = damage
        self.spell_range = spell_range

    def use(self, player, entities):
        results = []
        closest_monster = player.get_closest_entity_of_type(
            entities, EntityTypes.MONSTER)
        if (closest_monster and 
            player.distance_to(closest_monster) <= self.spell_range):
            text = 'A shining magic missile pierces the {}'.format(
                closest_monster.name)
            message = Message(text, COLORS.get('white'))
            results.append({'item_consumed': (True, self.owner),
                            'damage': (closest_monster, self.damage),
                            'message': message})
        else:
            message = Message(
                "A shining magic missile streaks into the darkness.",
                COLORS.get('white'))
            results.append({'item_consumed': (True, self.owner),
                            'damage': (closest_monster, self.damage),
                            'message': message})
        return results
