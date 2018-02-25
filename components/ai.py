class BasicMonster:

    def take_turn(self, target, game_map, entities):
        monster = self.owner
        if game_map.fov[monster.x, monster.y]:
            if monster.distance_to(target) >= 2:
                monster.move_towards(target.x, target.y, game_map, entities)
            elif target.fighter and target.fighter.hp > 0:
                print('The {0} insults you!'.format(monster.name))
