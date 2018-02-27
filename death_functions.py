from game_states import GameStates

def kill_player(player, colors):
    player.char = '%'
    player.color = colors.get('dark_red')
    return [{'message': 'You died!'}]

def kill_monster(monster, colors):
    monster.char = '%'
    monster.color = colors.get('dark_red')
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Remains of ' + monster.name
    return [{'message': '{} is dead!'.format(monster.name.capitalize())}]
