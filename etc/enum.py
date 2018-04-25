from enum import Enum, auto


#-----------------------------------------------------------------------------
# The various game states.
#
# The behaviour of the main game loop is governed by the value of the
# game_states variable, which must be one the values from this enumeration.
#.............................................................................
#
# ANIMATION_PLAYING:
#   An animation is currently playing.  Each tick of the game loop is used to
#   advance a frame in this animation.  All player and enemy actions are halted
#   until the animation completes.
# CURSOR_INPUT:
#   The selection cursor is currently displayed and under the users control.
#   All (other) player and enemy actions are halted until the user selects a
#   position on the map.
# DROP_INVENTORY:
#   The inventory screen is open for dropping items.
# ENEMY_TURN:
#   It is the enemy's turn to take action.
# PLAYER_DEAD:
#   The player is dead.
# PLAYER_TURN:
#   It is the player's turn to take action.
# SHOW_INVENTORY:
#   The inventory is open for using items.
#.............................................................................
class GameStates(Enum):
    ANIMATION_PLAYING = auto()
    CURSOR_INPUT = auto()
    DROP_INVENTORY = auto()
    ENEMY_TURN = auto() 
    PLAYER_DEAD = auto()
    PLAYER_TURN = auto() 
    #TODO: Change this name to USE_INVENTORY
    SHOW_INVENTORY = auto()
    THROW_INVENTORY = auto()


#-----------------------------------------------------------------------------
# The various results of actions and thier consequences in the game.
#
# The results of game actions, and their consequent effects on game state are
# governed by these catagories of consequences.  These are used as dictionary
# keys, with the associated values the data needed to update the game state as
# a result of these results.  These dictionaries are added to a stack (either
# player_turn_results or enemy_turn_results) for processing.  Results are
# processed until the stack is empty.
#.............................................................................
#
# ANIMATION: (Animation type, ... other data needed for specific animation)
#   Play an animation.
# CURSOR_MODE: boolean
#   Enter cursor mode.
# CURSOR_SELECT: boolean
#   The user has selected a map tile while in cursor model.
# DAMAGE: (entity, amount)
#   Deal damage to an entity
# DEAD_ENTITY: entity
#   An entity has died.
# DEATH_MESSAGE: Message object
#   A message that the player has died.  TODO: Depreciate this.
# DROP_INVENTORY: boolean
#   Open the inventory for dropping items.
# EXIT: boolean
#   Exit a menu, or the game.
# FULLSCREEN: boolean
#   Enter fullscreen mode.
# HEAL: (entity, amount)
#   Heal an entity a a given amount.
# INVENTORY_INDEX: int
#   The index of an item chosen from the player's inventory.
# ITEM_ADDED: item
#   Add an item to the the player's inventory.  TODO: This should work with any
#   entity.
# ITEM_CONSUMED: (bool, entity)
#   The entity has or has not consumed an item.
# ITEM_DROPPED: item
#   The player has dropped an item.  TODO: We should be able to drop an item in
#   a position.
# MESSAGE: message
#   Display a game message in the message queue.
# MOVE: (dx, dy) 
#   Move the player or another entity on the game map.
# PICKUP: bool 
#   Pickup an item at the current position.  TODO: This should work with any
#   entity.
# SHOW_INVENTORy: bool
#   Show the inventory menu.
#.............................................................................
class ResultTypes(Enum):
    ANIMATION = auto()
    CURSOR_MODE = auto()
    CURSOR_SELECT = auto()
    DAMAGE = auto()
    DEAD_ENTITY = auto()
    DEATH_MESSAGE = auto()
    DROP_INVENTORY = auto()
    EXIT = auto()
    FULLSCREEN = auto()
    HEAL = auto()
    INVENTORY_INDEX = auto()
    ITEM_ADDED = auto()
    ITEM_CONSUMED = auto()
    ITEM_DROPPED = auto()
    MESSAGE = auto()
    MOVE = auto()
    PICKUP = auto()
    SHOW_INVENTORY = auto()
    THROW_INVENTORY = auto()


class EntityTypes(Enum):
    PLAYER = 1
    MONSTER = 2
    ITEM = 3
    CORPSE = 4


class Animations(Enum):
    HEALTH_POTION = auto()
    MAGIC_MISSILE = auto()
    FIREBLAST = auto()
    THROWING_KNIFE = auto()


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


class ItemTargeting(Enum):
    PLAYER = auto()
    CLOSEST_MONSTER = auto()
    WITHIN_RADIUS = auto()
    FIRST_ALONG_PATH_TO_CURSOR = auto()


class ItemGroups(Enum):
    NONE = auto()
    ONE_HEALTH_POTION = auto()
    TWO_HEALTH_POTIONS = auto()
    MAGIC_MISSILE_SCROLL = auto()
    FIREBLAST_SCROLL = auto()
    THROWING_KNIFE = auto()


class MonsterGroups(Enum):
    NONE = auto()
    SINGLE_ORC = auto() 
    THREE_ORCS = auto() 
    SINGLE_TROLL = auto() 
    TWO_ORCS_AND_TROLL = auto()
    KRUTHIK_SQARM = auto()
