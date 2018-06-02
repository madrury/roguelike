from messages import Message
from status_bar import StatusBar
from game_events import fireblast, waterblast

from utils.utils import random_adjacent
from etc.enum import ResultTypes, Elements
from etc.config import PANEL_CONFIG 
from etc.game_config import (
    FIREBLOAT_BLAST_RADIUS, FIREBLOAT_BLAST_DAMAGE,
    WATERBLOAT_BLAST_RADIUS, WATERBLOAT_BLAST_DAMAGE)
from etc.colors import STATUS_BAR_COLORS

import game_objects.monsters


class Harmable:
    """Component for entities that can take damage.

    Attributes
    ----------
    max_hp: int
      The maximum hit points the entity can have.

    hp: int
      The current hit points the entity has.  When this drops to zero, a death
      event is triggered.

    defense: int
      The natural defense of this entity to resist damage.

    damage_callbacks: List[DamageFilter]
      A list of transformers to reduce (or increase) incoming damage.  Granted by
      armor or status.

    damage_transformers: List[DamageFilter]
      A list of callbacks to call when a damage event is triggered.  Useful for
      things like counterattacks, status triggers, etc.

    status_bar: StatusBar
      An object that can render a status bar, displaying the entities current hp.
    """
    def __init__(self, hp, defense, *,
                 damage_transformers=None,
                 damage_callbacks=None):
        self.max_hp = hp
        self.hp = hp
        self.status_bar = StatusBar(
            total_width=PANEL_CONFIG['bar_width'],
            bar_colors=STATUS_BAR_COLORS['hp_bar'])

    def harm(self, game_map, source, amount, elements):
        """Apply damage from an element or elements.

        It is not neccesarrly that the entity take all of the damage.  The
        entity may have equipment or resistances that grant them transformers for
        incomping damage.

        Damage can be responded to by providing callbacks in the
        damage_callbacks list.  These are called whenver this method is called.
        """
        results = []
        self.hp = max(0, self.hp - amount)
        if self.hp <= 0:
            results.append({ResultTypes.DEAD_ENTITY: self.owner})
        return results

    # TODO: Remove this method.
    def heal(self, amount):
        """Restore some amount of hp."""
        self.hp += min(amount, self.max_hp - self.hp)

    def add_damage_transformers(self, transformers):
        for transformer in transformers:
            self.damage_transformers.append(transformer)

    def remove_damage_transformers(self, transformers):
        for transformer in transformers:
            self.damage_transformers.remove(transformer)

    def add_damage_callbacks(self, callbacks):
        for callback in callbacks:
            self.damage_callbacks.append(callback)

    def remove_damage_callbacks(self, callbacks):
        for callback in callbacks:
            self.damage_callbacks.remove(callback)

    def render_status_bar(self, panel, x, y):
        self.status_bar.render(
            panel, x, y, 
            name=self.owner.name + ' HP',
            maximum=self.max_hp,
            value=self.hp)


class PinkJellyHarmable(Harmable):
    """Spawns another copy of a Pink Jelly in a random adjacent space when
    harmed.
    """
    def harm(self, game_map, source, amount, elements):
        results = []
        self.hp = max(0, self.hp - amount)
        if self.hp > 0:
            x, y = random_adjacent((self.owner.x, self.owner.y))
            jelly = game_objects.monsters.PinkJelly.make_if_possible(
                game_map, x, y, hp=self.hp)
            if jelly:
                results.append({ResultTypes.ADD_ENTITY: jelly})
        if self.hp <= 0:
            results.append({ResultTypes.DEAD_ENTITY: self.owner})
        return results


class FireBloatHarmable(Harmable):
    """Explodes into a fireblast when harmed."""
    def harm(self, game_map, source, amount, elements):
        results = []
        if Elements.WATER not in elements:
            results.extend(fireblast(
                game_map,
                (self.owner.x, self.owner.y),
                radius=FIREBLOAT_BLAST_RADIUS,
                damage=FIREBLOAT_BLAST_DAMAGE))
        results.append({ResultTypes.DEAD_ENTITY: self.owner})
        return results


class WaterBloatHarmable(Harmable):
    """Explodes into a water when harmed."""
    def harm(self, game_map, source, amount, elements):
        results = []
        results.extend(waterblast(
            game_map,
            (self.owner.x, self.owner.y),
            radius=WATERBLOAT_BLAST_RADIUS,
            damage=WATERBLOAT_BLAST_DAMAGE))
        results.append({ResultTypes.DEAD_ENTITY: self.owner})
        return results


class NullHarmable:

    def harm(self, game_map, source, amount, elements):
        return []

    def heal(self, amount, elements):
        return []

    def render_status_bar(self, panel, x, y):
        pass

    def __bool__(self):
        """Prevent entities with this component from showing up in searches for
        harmable entities.
        """
        return False
