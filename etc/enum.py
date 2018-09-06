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
# EQUIP_INVENTORY:
#   The inventory screen is open for equipping items.
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
    EQUIP_INVENTORY = auto()
    PLAYER_DEAD = auto()
    PLAYER_TURN = auto()
    POST_PLAYER_TURN = auto()
    #TODO: Change this name to USE_INVENTORY
    SHOW_INVENTORY = auto()
    THROW_INVENTORY = auto()

# Game states where an inventory is displayed.
INVENTORY_STATES = {
    GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY,
    GameStates.THROW_INVENTORY, GameStates.EQUIP_INVENTORY}

# Game states accepting of user input.
INPUT_STATES = {
    GameStates.PLAYER_TURN, GameStates.SHOW_INVENTORY,
    GameStates.DROP_INVENTORY, GameStates.THROW_INVENTORY,
    GameStates.EQUIP_INVENTORY, GameStates.CURSOR_INPUT,
    GameStates.PLAYER_DEAD}

# Game states that can be canceled out of.
CANCEL_STATES = {
    GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY,
    GameStates.THROW_INVENTORY, GameStates.EQUIP_INVENTORY,
    GameStates.CURSOR_INPUT}

class ResultTypes(Enum):
    """The various results of turn actions.

    The results of game actions, and their consequent effects on game state are
    enumerated by these catagories.

    The elements of this enum are used as dictionary keys in dictionaries
    returned from components responsible for processing in game actions and
    consequences. The values in these dictionries store the data needed to
    update the game state as a result.  In the main game loop, these
    dictionaries are added to a stack (either player_turn_results or
    enemy_turn_results) for processing.  Results are processed until the stack
    is empty.

    Enum Elements:
    --------------
    ADD_ENTITY: entity
        Add an entity to the game map.
    ADD_ITEM_TO_INVENTORY: (item, entity)
        Add an item to the entity's inventory.
    ANIMATION: (Animation type, ... other data needed for specific animation)
        Play an animation.
    CONFUSE: entity
        Put the entity in a confused state.
    CURSOR_MODE: boolean
        Enter cursor mode.
    DAMAGE: (entity, source, amount, elements)
        Deal damage to an entity of some elemental types.  Note that this
        damage is not immediately commited, instead it may be further processed
        due to defensive characteristics of teh target entity.  For commited
        damage, see the HARM result type.
    DEAD_ENTITY: entity
        An entity has died.
    DEATH_MESSAGE: Message object
        A message that the player has died.  TODO: Depreciate this.
    # TODO: Rename to CONSUME_ITEM
    DISCARD_ITEM: (entity, bool)
        The entity has or has not consumed an item.
    DOUBLE_SPEED: entity
        Double the entities speed for a duration of turns.
    END_TURN: bool
        End the player's turn.
    EQUIP: (equipable_entity, entity):
        Equip equipable_entity onto entity.
    EQUIP_INVENTORY: boolean
        Open the inventory for equipping items.
    FREEZE: entity
        Freeze an entity.
    ITEM_DROPPED: item
        The player has dropped an item.  TODO: We should be able to drop an
        item in a position.
    MESSAGE: message
        Display a game message in the message queue.
    MOVE_TOWARDS: entity, target_x, target_y
        Attempt to move the entity towards the target.
    MOVE_RANDOM_ADJACENT: entity
        Attempt to move the entity to a random adjacent square.
    """
    # We need this enum to have an order, since there are certain turn results
    # that must be processed first.
    def __lt__(self, other):
        return self.value < other.value

    ADD_ENTITY = auto()
    ADD_ITEM_TO_INVENTORY = auto()
    CHANGE_SWIM_STAMINA = auto()
    CONFUSE = auto()
    DAMAGE = auto()
    DEAD_ENTITY = auto()
    DEATH_MESSAGE = auto()
    DISCARD_ITEM = auto()
    DOUBLE_SPEED = auto()
    DROP_ITEM_FROM_INVENTORY = auto()
    END_TURN = auto()
    EQUIP_ARMOR = auto()
    EQUIP_WEAPON = auto()
    FREEZE = auto()
    HARM = auto()
    INCREASE_ATTACK_POWER = auto()
    MESSAGE = auto()
    MOVE = auto()
    MOVE_RANDOM_ADJACENT = auto()
    MOVE_TOWARDS = auto()
    RECHARGE_ITEM = auto()
    REMOVE_ARMOR = auto()
    REMOVE_ENTITY = auto()
    REMOVE_WEAPON = auto()
    RESTORE_PLAYER_INPUT = auto()
    SET_POSITION = auto()
    # This must be processed before any healing (which is passed as a DAMAGE
    # message).
    INCREASE_MAX_HP = 90
    # These two must be processed first!
    ANIMATION = 99
    CURSOR_MODE = 98


class FloorResultTypes(Enum):
    """Enumerates the outcomes from a dungeon floor."""
    # Note these are reversed because DEEPER floors are numbered higher.
    INCREMENT_FLOOR = -1
    DECREMENT_FLOOR = +1
    END_GAME = auto()


class InputTypes(Enum):
    CURSOR_SELECT = auto()
    DROP_INVENTORY = auto()
    EQUIP_INVENTORY = auto()
    EXIT = auto()
    FULLSCREEN = auto()
    INVENTORY_INDEX = auto()
    MOVE = auto()
    PICKUP = auto()
    SHOW_INVENTORY = auto()
    THROW_INVENTORY = auto()


class EntityTypes(Enum):
    PLAYER = auto()
    MONSTER = auto()
    ITEM = auto()
    CORPSE = auto()
    TERRAIN = auto()
    FIRE = auto()
    STEAM = auto()


class TreeStates(Enum):
    SUCCESS = auto()
    FAILURE = auto()
    RUNNING = auto()


class CursorTypes(Enum):
    PATH = auto()
    RAY = auto()
    ADJACENT = auto()


class Animations(Enum):
    CONCATINATED = auto()
    CONFUSION_POTION = auto()
    FIREBALL = auto()
    FIREBLAST = auto()
    HEALTH_POTION = auto()
    ICEBALL = auto()
    MAGIC_MISSILE = auto()
    POWER_POTION = auto()
    SIMULTANEOUS = auto()
    SPEED_POTION = auto()
    THROWING_KNIFE = auto()
    THROW_POTION = auto()
    WATERBLAST = auto()


class Terrain(Enum):
    POOL = auto()
    ICE_PATCH = auto()
    GRASS = auto()
    SHRUBS = auto()


class RenderOrder(Enum):
    TERRAIN = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4


class ItemTargeting(Enum):
    PLAYER = auto()
    CLOSEST_MONSTER = auto()
    WITHIN_RADIUS = auto()
    FIRST_ALONG_PATH_TO_CURSOR = auto()


class Elements(Enum):
    NONE = auto()
    HEALING = auto()
    FIRE = auto()
    ICE = auto()
    WATER = auto()
    NECROTIC = auto()


class RoutingOptions(Enum):
    AVOID_DOORS = auto()
    AVOID_FIRE = auto()
    AVOID_MONSTERS = auto()
    AVOID_SHRUBS = auto()
    AVOID_STAIRS = auto()
    AVOID_STEAM = auto()
    AVOID_WATER = auto()


class ItemGroups(Enum):
    NONE = auto()
    ONE_HEALTH_POTION = auto()
    POWER_POTION = auto()
    TWO_HEALTH_POTIONS = auto()
    MAGIC_MISSILE_SCROLL = auto()
    FIREBLAST_SCROLL = auto()
    WATERBLAST_SCROLL = auto()
    THROWING_KNIFE = auto()
    FIRE_STAFF = auto()
    LANCE = auto()
    SWORD = auto()
    AXE = auto()
    LEATHER_ARMOR = auto()
    LEATHER_ARMOR_OF_FIRE_RESIST = auto()
    REFLECT_SUIT = auto()


class MonsterGroups(Enum):
    NONE = auto()
    SINGLE_ORC = auto()
    THREE_ORCS = auto()
    SINGLE_TROLL = auto()
    TWO_ORCS_AND_TROLL = auto()
    KRUTHIK_SQARM = auto()
    PINK_JELLY = auto()
    FIRE_BLOAT = auto()
    WATER_BLOAT = auto()
    ZOMBIE = auto()
    NECROMANCER = auto()
