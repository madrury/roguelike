class BasicMonster:

    def take_turn(self, target, game_map):
        results = []
        monster = self.owner
        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                results.append({'move_towards': (monster, target.x, target.y)})
            elif target.fighter and target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)
        return results
