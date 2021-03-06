from etc.enum import ResultTypes

from components.behaviour_trees.root import Root
from components.behaviour_trees.composite import (
    Selection, Sequence, Negate)
from components.behaviour_trees.leaf import (
     Attack, MoveTowardsTargetEntity, Skitter, TravelToRandomPosition,
     SeekTowardsLInfinityRadius, SpawnEntity, DoNothing,
     MoveTowardsPointInNamespace)
from components.behaviour_trees.conditions import (
    IsAdjacent, WithinFov, WithinL2Radius, AtLInfinityRadius, CoinFlip,
    InNamespace)

import game_objects.monsters


class BaseAI:
    """Base class for creature AI.
    
    Creature's behaviour is defined by a behaviour tree, stored in the tree
    attribute.  Behaviour trees have a tick method, which is called when the
    reature takes a turn.  The tick method returns a turn result dictionary
    that summarizes the turn's effect on the game state.
    """
    def take_turn(self, game_map):
        _, results = self.tree.tick(self.owner, game_map)
        return results

    def set_target(self, target):
        self.tree.namespace["target"] = target


class BasicMonster(BaseAI):
    """Simple monster ai.

    When in the targets POV, attempt to move towards the target.  If adjacent
    to the target, attack.
    """
    def __init__(self):
        self.tree = Root(
            Selection(
                Sequence(
                    IsAdjacent(),
                    Attack()),
                Sequence(
                    WithinFov(),
                    MoveTowardsTargetEntity(target_point_name="target_point")),
                Sequence(
                    InNamespace(name="target_point"),
                    MoveTowardsPointInNamespace(name="target_point")),
                TravelToRandomPosition()))


class ConfusedMonster(BaseAI):
    """AI for a confused monster.

    Always move to a random adjacent space.
    """
    def __init__(self):
        self.tree = Root(Skitter())


class FrozenMonster(BaseAI):
    """AI for a frozen monster.

    Always passes the turn without acting.
    """
    def __init__(self):
        self.tree = Root(DoNothing())


class NecromancerMonster(BaseAI):
    """AI for a necromancer.

    Necromancers attempt to always stay at exactly a given radius of the
    target.  If they fall within the radius, they will move away, if they fall
    outside the radius, they will move towards.  When they are at exactly the
    desired radius, they will spawn a zombie with a certain probability.
    """
    def __init__(self, move_towards_radius=6, seeking_radius=3):
        self.tree = Root(
            Selection(
                Sequence(
                    AtLInfinityRadius(radius=seeking_radius),
                    CoinFlip(p=0.3),
                    SpawnEntity(game_objects.monsters.Zombie)),
                Sequence(
                    WithinL2Radius(radius=move_towards_radius),
                    SeekTowardsLInfinityRadius(radius=seeking_radius)),
                TravelToRandomPosition()))


class HuntingMonster(BaseAI):
    """A more dangerous monster.

    Attempts to move towards the target even if not in the targets POV.
    """
    def __init__(self, sensing_range=12):
        self.sensing_range = sensing_range
        self.tree = Root(
            Selection(
                Sequence(
                    IsAdjacent(),
                    Attack()),
                Sequence(
                    WithinL2Radius(radius=sensing_range),
                    MoveTowardsTargetEntity(target_point_name="target_point")),
                TravelToRandomPosition()))


class ZombieMonster(BaseAI):
    """Similar to a HuntingMonster, but will not wander."""
    def __init__(self, move_towards_radius=6):
        self.tree = Root(
            Selection(
                Sequence(
                    IsAdjacent(),
                    Attack()),
                Sequence(
                    WithinL2Radius(radius=move_towards_radius),
                    MoveTowardsTargetEntity(target_point_name="target_point"))))


class SkitteringMonster(BaseAI):
    """An impatient monster.

    When close by, attempts to move towards the target.  Otherwise, moves to a
    random adjacent square.
    """
    def __init__(self, skittering_range=3):
        self.skittering_range = skittering_range
        self.tree = Root(
            Selection(
                Sequence(
                    IsAdjacent(),
                    Attack()),
                Sequence(
                    WithinL2Radius(radius=skittering_range),
                    MoveTowardsTargetEntity(target_point_name="target_point")),
                Skitter()))
