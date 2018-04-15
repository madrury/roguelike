from enum import Enum, auto

class GameStates(Enum):
    PLAYER_TURN = 1
    ENEMY_TURN = 2
    PLAYER_DEAD = 3
    SHOW_INVETORY = 4
    DROP_INVENTORY = 5


class EntityTypes(Enum):
    PLAYER = auto()
    MONSTER = auto()
    ITEM = auto()
    CORPSE = auto()


class ItemTargeting(Enum):
    PLAYER = auto()
    CLOSEST_MONSTER = auto()


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


class ItemGroups(Enum):
    NONE = auto()
    ONE_HEALTH_POTION = auto()
    TWO_HEALTH_POTIONS = auto()
    MAGIC_MISSILE_SCROLL = auto()


class MonsterGroups(Enum):
    NONE = auto()
    SINGLE_ORC = auto() 
    THREE_ORCS = auto() 
    SINGLE_TROLL = auto() 
    TWO_ORCS_AND_TROLL = auto()
    KRUTHIK_SQARM = auto()
