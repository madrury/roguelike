from etc.enum import EntityTypes, GameStates, RenderOrder
from game_messages import Message

def kill_player(player, colors):
    player.char = '%'
    player.color = colors.get('dark_red')
    return [{'death_message': Message('You died!', colors['red'])}]

def kill_monster(monster, colors):
    monster.blocks = False
    monster.attacker = None
    monster.harmable = None
    monster.ai = None
    message = '{} is dead!'.format(monster.name.capitalize())
    return [{'death_message': Message(message, colors['orange'])}]

def make_corpse(monster, colors):
    monster.char = '#'
    monster.color = colors.get('dark_red')
    monster.entity_type = EntityTypes.CORPSE
    monster.name = 'Remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE
