from game_messages import Message

class Item:

    def __init__(self):
        pass

class HealthPotion:

    def __init__(self, healing=5):
        self.use_on_player = True
        self.healing = healing

    def use(self, player, colors):
        results = []
        if player.fighter.hp == player.fighter.max_hp:
            message = Message('You are already at full health.', 
                              colors.get('white'))
            results.append({'item_consumed': (False, self.owner), 
                            'message': message})
        else:
            message = Message('You wounds start to heal.', 
                              colors.get('green'))
            results.append({'item_consumed': (True, self.owner),
                            'heal': (player, self.healing),
                            'message': message})
        return results
            
