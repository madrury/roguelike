from tdl.map import Map
import numpy as np
from random import randint, choice

from entity import Entity
from render_functions import RenderOrder

from .floor import random_dungeon_floor

from components.ai import BasicMonster
from components.attacker import Attacker
from components.harmable import Harmable
from components.item import HealthPotion


class GameMap(Map):

    def __init__(self, width, height):
        super().__init__(width, height)
        self.explored = np.zeros((width, height)).astype(bool)

    def make_transparent_and_walkable(self, x, y):
        self.walkable[x, y] = True
        self.transparent[x, y] = True


# TODO: Transition these to thier own files.
def generate_monsters(game_map, rooms, enitities, map_config, colors):
    return _generate_entities(
        game_map, rooms, enitities, map_config['max_monsters_per_room'],
        _make_random_monster, colors)

def generate_items(game_map, rooms, enitities, map_config, colors):
    return _generate_entities(
        game_map, rooms, enitities, map_config['max_items_per_room'],
        _make_random_item, colors)

def _generate_entities(game_map, rooms, entities, max_new_entities_per_room, 
                      entity_generator, colors):
    new_entities = []
    for room in rooms:
        number_of_new_entities = randint(0, max_new_entities_per_room)
        for _ in range(number_of_new_entities):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            entity_at_position = any(
                entity for entity in entities 
                if entity.x == x and entity.y == y)
            new_entity_at_position = any(
                entity for entity in new_entities
                if entity.x == x and entity.y == y)
            if (game_map.walkable[x, y] 
                and (not entity_at_position)
                and (not new_entity_at_position)):
                new_entity = entity_generator(x, y, colors)
                new_entities.append(new_entity)
    return new_entities
def _make_random_monster(x, y, colors):
    if randint(0, 100) < 80:
        monster = Entity(
            x, y, 'O', colors['desaturated_green'], 'Orc', 
            attacker=Attacker(power=3),
            harmable=Harmable(hp=10, defense=0),
            ai=BasicMonster(),
            blocks=True,
            render_order=RenderOrder.ACTOR)
    else:
        monster = Entity(
            x, y, 'T', colors['darker_green'], 'Troll', 
            attacker=Attacker(power=4),
            harmable=Harmable(hp=16, defense=1),
            ai=BasicMonster(),
            blocks=True,
            render_order=RenderOrder.ACTOR)
    return monster

def _make_random_item(x, y, colors):
    return Entity(x, y, '!', colors['violet'], 'Healing Potion',
                  render_order=RenderOrder.ITEM,
                  item=HealthPotion())
