from etc.enum import ResultTypes
from utils.utils import distance_to

from components.behaviour_trees.composite import (
    Selection, Sequence, Negate)
from components.behaviour_trees.leaf import (
     Attack, MoveTowards, Skitter, TravelToRandomPosition,
     SeekTowardsLInfinityRadius, SpawnEntity)
from components.behaviour_trees.conditions import (
    IsAdjacent, WithinFov, WithinRadius, AtLInfinityRadius, CoinFlip)

import game_objects.monsters


class BasicMonster:
    """Simple monster ai.

    When in the players POV, attempt to move towards the player.  If adjacent
    to the player, attack.
    """
    def __init__(self):
        self.tree = Selection(
            Sequence(
                IsAdjacent(),
                Attack()),
            Sequence(
                WithinFov(),
                MoveTowards()),
            TravelToRandomPosition())

    def take_turn(self, target, game_map):
        _, results = self.tree.tick(self.owner, target, game_map, {})
        return results


class NecromancerMonster:

    def __init__(self, move_towards_radius=6, seeking_radius=3):
        self.tree = Selection(
            Sequence(
                AtLInfinityRadius(radius=seeking_radius),
                CoinFlip(p=0.3),
                SpawnEntity(game_objects.monsters.Zombie)),
            Sequence(
                WithinRadius(radius=move_towards_radius),
                SeekTowardsLInfinityRadius(radius=seeking_radius)),
            TravelToRandomPosition())

    def take_turn(self, target, game_map):
        _, results = self.tree.tick(self.owner, target, game_map, {})
        return results


class HuntingMonster:
    """A more dangerous monster.

    Attempts to move towards the player even if not in the players POV.
    """
    def __init__(self, sensing_range=12):
        self.sensing_range = sensing_range
        self.tree = Selection(
            Sequence(
                IsAdjacent(),
                Attack()),
            Sequence(
                WithinRadius(radius=sensing_range),
                MoveTowards()),
            TravelToRandomPosition())

    def take_turn(self, target, game_map):
        _, results = self.tree.tick(self.owner, target, game_map, {})
        return results


class ZombieMonster:
    """Similar to a HuntingMonster, but will not wander."""
    def __init__(self, move_towards_radius=6):
        self.tree = Selection(
            Sequence(
                IsAdjacent(),
                Attack()),
            Sequence(
                WithinRadius(radius=move_towards_radius),
                MoveTowards()))

    def take_turn(self, target, game_map):
        _, results = self.tree.tick(self.owner, target, game_map, {})
        return results


class SkitteringMonster:
    """An impatient monster.

    When close by, attempts to move towards the player.  Otherwise, moves to a
    random adjacent square.
    """
    def __init__(self, skittering_range=3):
        self.skittering_range = skittering_range
        self.tree = Selection(
            Sequence(
                IsAdjacent(),
                Attack()),
            Sequence(
                WithinRadius(radius=skittering_range),
                MoveTowards()),
            Skitter())

    def take_turn(self, target, game_map):
        _, results = self.tree.tick(self.owner, target, game_map, {})
        return results
