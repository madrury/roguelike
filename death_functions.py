from etc.enum import EntityTypes, GameStates, RenderOrder, ResultTypes
from messages import Message

def kill_player(player, colors):
    player.char = '%'
    player.color = colors.get('dark_red')
    return [{ResultTypes.DEATH_MESSAGE: Message('You died!', colors['red'])}]

def kill_monster(monster, colors):
    monster.blocks = False
    monster.attacker = None
    monster.harmable = None
    monster.ai = None
    message = 'The {} is dead!'.format(monster.name.capitalize())
    return [{ResultTypes.MESSAGE: Message(message, colors['orange'])}]

def make_corpse(monster, colors):
    print("Drawing ", monster.name, " as a corpse.")
    monster.char = '#'
    monster.color = colors.get('dark_red')
    monster.entity_type = EntityTypes.CORPSE
    monster.name = 'Remains of the' + monster.name.capitalize()
    monster.render_order = RenderOrder.CORPSE
