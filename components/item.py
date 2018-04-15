from enum import Enum, auto

from game_messages import Message
from etc.colors import COLORS


class ItemTargeting(Enum):
    PLAYER = auto()
    CLOSEST_MONSTER = auto()


class ItemComponent:
    pass

class HealthPotionComponent(ItemComponent):

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
