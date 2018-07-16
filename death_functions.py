from messages import Message

from etc.enum import EntityTypes, GameStates, RenderOrder, ResultTypes
from etc.colors import COLORS

from components.harmable import NullHarmable
from components.floatable import Floatable


def kill_player(player):
    player.char = '%'
    player.color = COLORS['dark_red']
    return [{ResultTypes.DEATH_MESSAGE: Message('You died!', COLORS['red'])}]

def kill_monster(monster, game_map):
    game_map.blocked[monster.x, monster.y] = False
    monster.blocks = False
    # The corpse needs to be able to float, and so needs to pass checks for
    # movability into a water tile.
    monster.routing_avoid = []
    # Remove all monster components, or replace with null placeholders.
    monster.ai = None
    monster.attacker = None
    monster.burnable = None
    monster.status_manager = None
    monster.dissapatable = None
    monster.spreadable = None
    monster.swimable = None
    monster.floatable = Floatable()
    monster.floatable.owner = monster
    monster.harmable = NullHarmable()
    monster.harmable.owner = monster
    message = 'The {} is dead!'.format(monster.name.capitalize())
    return [{ResultTypes.MESSAGE: Message(message, COLORS['orange'])}]

def make_corpse(monster):
    monster.char = '#'
    monster.fg_color = COLORS['dark_red']
    monster.entity_type = EntityTypes.CORPSE
    monster.name = 'Remains of the ' + monster.name.capitalize()
    monster.render_order = RenderOrder.CORPSE
