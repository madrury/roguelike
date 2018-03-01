from game_states import GameStates
from game_messages import Message

def kill_player(player, colors):
    player.char = '%'
    player.color = colors.get('dark_red')
    return [{'death_message': Message('You died!', colors['red'])}]

def kill_monster(monster, colors):
    message = '{} is dead!'.format(monster.name.capitalize())
    monster.char = '%'
    monster.color = colors.get('dark_red')
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'Remains of ' + monster.name
    return [{'death_message': Message(message, colors['orange'])}]
