from enum import Enum, auto

class GameStates(Enum):
    ANIMATION_FINISHED = auto()
    ANIMATION_PLAYING = auto()
    DROP_INVENTORY = auto()
    ENEMY_TURN = auto() 
    PLAYER_DEAD = auto()
    PLAYER_TURN = auto() 
    SHOW_INVENTORY = auto()


class ResultTypes(Enum):
    ANIMATION = auto()
    DAMAGE = auto()
    DEAD_ENTITY = auto()
    DEATH_MESSAGE = auto()
    HEAL = auto()
    ITEM_ADDED = auto()
    ITEM_CONSUMED = auto()
    ITEM_DROPPED = auto()
    MESSAGE = auto()
    MOVE = auto()
    PICKUP = auto()
    DROP = auto()
    INVENTORY_INDEX = auto()
    SHOW_INVENTORY = auto()
    DROP_INVENTORY = auto()
    FULLSCREEN = auto()
    EXIT = auto()


class EntityTypes(Enum):
    PLAYER = 1
    MONSTER = 2
    ITEM = 3
    CORPSE = 4


class Animations(Enum):
    HEALTH_POTION = auto()
    MAGIC_MISSILE = auto()
    FIREBLAST = auto()


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


class ItemTargeting(Enum):
    PLAYER = auto()
    CLOSEST_MONSTER = auto()
    WITHIN_RADIUS = auto()


class ItemGroups(Enum):
    NONE = auto()
    ONE_HEALTH_POTION = auto()
    TWO_HEALTH_POTIONS = auto()
    MAGIC_MISSILE_SCROLL = auto()
    FIREBLAST_SCROLL = auto()


class MonsterGroups(Enum):
    NONE = auto()
    SINGLE_ORC = auto() 
    THREE_ORCS = auto() 
    SINGLE_TROLL = auto() 
    TWO_ORCS_AND_TROLL = auto()
    KRUTHIK_SQARM = auto()
