from enum import Enum, auto
import numpy as np

from entity import Entity
from render_functions import RenderOrder

from components.ai import BasicMonster
from components.attacker import Attacker
from components.harmable import Harmable

# TODO: Move this to a static directory.
COLORS = {
    'dark_wall': (0, 0, 100),
    'dark_ground': (50, 50, 150),
    'light_wall': (130, 110, 50),
    'light_ground': (200, 180, 50),
    'desaturated_green': (63, 127, 63),
    'darker_green': (0, 127, 0),
    'dark_red': (191, 0, 0),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'orange': (255, 127, 0),
    'light_red': (255, 144, 144),
    'darker_red': (127, 0, 0),
    'violet': (127, 0, 255),    
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'green': (0, 255, 0)
}

class Monsters(Enum):
    ORC = auto() 
    TROLL = auto()


class MonsterGroups(Enum):
    NONE = auto()
    SINGLE_ORC = auto() 
    THREE_ORCS = auto() 
    SINGLE_TROLL = auto() 
    TWO_ORCS_AND_TROLL = auto()


def spawn_monsters(monster_schedule, floor, entities):

    def choose_from_list_of_tuples(list_of_tuples):
        probs, choices = zip(*list_of_tuples)
        return np.random.choice(choices, size=1, p=probs)[0]

    for room in floor.rooms:
        monster_group = choose_from_list_of_tuples(MONSTER_SCHEDULE)
        spawn_monster_group(monster_group, room, entities)


def spawn_monster_group(monster_group, room, entities):
    for monster_type in MONSTER_GROUPS[monster_group]:
        monster = monster_type.spawn(room, entities)
        if monster is not None:
            entities.append(monster)


class Monster:

    @classmethod
    def spawn(cls, room, entities, max_tries=25):
        for _ in range(max_tries):
            x, y = room.random_point()
            if not any((x, y) == (entity.x, entity.y) for entity in entities):
                monster = cls.make(x, y)
                break
        else:
            monster = None
        return monster


class Orc(Monster):
    
    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'O', COLORS['desaturated_green'], 'Orc', 
            attacker=Attacker(power=3),
            harmable=Harmable(hp=10, defense=0),
            ai=BasicMonster(),
            blocks=True,
            render_order=RenderOrder.ACTOR)


class Troll(Monster):
         
    @staticmethod
    def make(x, y):
        return Entity(
            x, y, 'T', COLORS['darker_green'], 'Troll', 
            attacker=Attacker(power=4),
            harmable=Harmable(hp=16, defense=1),
            ai=BasicMonster(),
            blocks=True,
            render_order=RenderOrder.ACTOR)
            

MONSTER_GROUPS = {
    MonsterGroups.NONE: [],
    MonsterGroups.SINGLE_ORC: [Orc],
    MonsterGroups.THREE_ORCS: [Orc, Orc, Orc],
    MonsterGroups.SINGLE_TROLL: [Troll],
    MonsterGroups.TWO_ORCS_AND_TROLL: [Orc, Orc, Orc]
}


MONSTER_SCHEDULE = [
    (0.5, MonsterGroups.NONE),
    (0.5*0.4, MonsterGroups.SINGLE_ORC),
    (0.5*0.2, MonsterGroups.THREE_ORCS),
    (0.5*0.2, MonsterGroups.SINGLE_TROLL),
    (0.5*0.2, MonsterGroups.TWO_ORCS_AND_TROLL),
]
