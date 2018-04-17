from enum import Enum, auto

class GameStates(Enum):
    PLAYER_TURN = auto() 
    ENEMY_TURN = auto() 
    PLAYER_DEAD = auto()
    SHOW_INVETORY = auto()
    DROP_INVENTORY = auto()
    ANIMATION_PLAYING = auto()
    ANIMATION_FINISHED = auto()


class EntityTypes(Enum):
    PLAYER = auto()
    MONSTER = auto()
    ITEM = auto()
    CORPSE = auto()


class ItemTargeting(Enum):
    PLAYER = auto()
    CLOSEST_MONSTER = auto()
    WITHIN_RADIUS = auto()


class RenderOrder(Enum):
    CORPSE = auto()
    ITEM = auto()
    ACTOR = auto()


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


class Animations(Enum):
    HEALTH_POTION = auto()
    MAGIC_MISSILE = auto()
    FIREBLAST = auto()
