class BasicMonster:

    def take_turn(self, target, game_map):
        results = []
        monster = self.owner
        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                results.append({'move_towards': (monster, target.x, target.y)})
            elif target.harmable and target.harmable.hp > 0:
                attack_results = monster.attacker.attack(target)
                results.extend(attack_results)
        return results
