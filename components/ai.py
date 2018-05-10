from etc.enum import ResultTypes

class BasicMonster:
    """Simple monster ai.

    When in the players POV, attempt to move towards the player.  If adjacent
    to the player, attack.
    """
    def take_turn(self, target, game_map):
        results = []
        monster = self.owner
        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                results.append({ResultTypes.MOVE_TOWARDS: (monster, target.x, target.y)})
            elif target.harmable and target.harmable.hp > 0:
                attack_results = monster.attacker.attack(target)
                results.extend(attack_results)
        return results


class HuntingMonster:
    """A more dangerous monster.

    Attempts to move towards the player even if not in the players POV.
    """
    def __init__(self, sensing_range=12):
        self.sensing_range = sensing_range

    def take_turn(self, target, game_map):
        results = []
        monster = self.owner
        if 2 <= monster.distance_to(target) <= self.sensing_range:
            results.append({ResultTypes.MOVE_TOWARDS: (monster, target.x, target.y)})
        elif (monster.distance_to(target) <= 2 and 
              target.harmable and target.harmable.hp > 0):
            attack_results = monster.attacker.attack(target)
            results.extend(attack_results)
        return results


class SkitteringMonster:
    """An impatient monster.

    When close by, attempts to move towards the player.  Otherwise, moves to a
    random adjacent square.
    """
    def __init__(self, skitering_range=3):
        self.skitering_range = skitering_range

    def take_turn(self, target, game_map):
        results = []
        monster = self.owner
        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) > self.skitering_range:
                results.append({ResultTypes.MOVE_RANDOM_ADJACENT: monster})
            elif monster.distance_to(target) <= self.skitering_range:
                results.append({ResultTypes.MOVE_TOWARDS: (monster, target.x, target.y)})
        return results
