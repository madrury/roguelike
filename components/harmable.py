from messages import Message
from status_bar import StatusBar
from utils.utils import random_adjacent
from etc.enum import ResultTypes, Elements
from etc.config import PANEL_CONFIG 
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

    damage_transformers: List[DamageFilter]
      A list of transformers to reduce (or increase) incoming damage.  Granted by
      armor or status.

    status_bar: StatusBar
      An object that can render a status bar, displaying the entities current hp.
    """
    def __init__(self, hp, defense, damage_transformers=None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.damage_transformers = []
        if damage_transformers:
            for transformer in damage_transformers:
                self.damage_transformers.append(transformer)
        self.status_bar = StatusBar(
            total_width=PANEL_CONFIG['bar_width'],
            bar_colors=STATUS_BAR_COLORS['hp_bar'])

    def harm(self, game_map, amount, elements):
        """Apply damage from an element or elements.

        It is not neccesarrly that the entity take all of the damage.  The
        entity may have equipment or resistances that grant them transformers for
        incomping damage.
        """
        for transformer in self.damage_transformers:
            amount = transformer.transform_damage(amount, elements)
        self.hp -= amount
        results = []
        if self.hp <= 0:
            results.append({ResultTypes.DEAD_ENTITY: self.owner})
        return results

    def heal(self, amount):
        """Restore some amount of hp."""
        self.hp += min(amount, self.max_hp - self.hp)

    def add_damage_transformers(self, transformers):
        for transformer in transformers:
            self.damage_transformers.append(transformer)

    def remove_damage_transformers(self, transformers):
        for transformer in transformers:
            self.damage_transformers.remove(transformer)

    def render_status_bar(self, panel, x, y):
        self.status_bar.render(
            panel, x, y, 
            name=self.owner.name + ' HP',
            maximum=self.max_hp,
            value=self.hp)


class PinkJellyHarmable(Harmable):

    def harm(self, game_map, amount, elements):
        for transformer in self.damage_transformers:
            amount = transformer.transform_damage(amount, elements)
        self.hp -= amount
        results = []
        if self.hp > 0:
            # Spawn a new jelly with the same hp.
            x, y = random_adjacent((self.owner.x, self.owner.y))
            jelly = game_objects.monsters.PinkJelly.make_if_possible(
                game_map, x, y, hp=self.hp)
            results.append({ResultTypes.ADD_ENTITY: jelly})
        if self.hp <= 0:
            results.append({ResultTypes.DEAD_ENTITY: self.owner})
        return results


class NullHarmable:

    def harm(self, game_map, amount, elements):
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
