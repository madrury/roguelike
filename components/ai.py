from etc.enum import ResultTypes
from utils.utils import distance_to

from behaviour_tree import (
    Selection, Sequence, Negate, IsAdjacent, WithinFov, Attack, MoveTowards, 
    WithinRadius, Skitter)


class BasicMonster:
    """Simple monster ai.

    When in the players POV, attempt to move towards the player.  If adjacent
    to the player, attack.
    """
    tree = Selection(
        Sequence(
            IsAdjacent(),
            Attack()),
        Sequence(
            WithinFov(),
            MoveTowards()))

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
