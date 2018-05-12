from messages import Message
from etc.enum import ResultTypes, Elements
from etc.config import PANEL_CONFIG 
from etc.colors import STATUS_BAR_COLORS
from status_bar import StatusBar


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

    damage_filters: List[DamageFilter]
      A list of filters to reduce (or increase) incoming damage.  Granted by
      armor or status.

    status_bar: StatusBar
      An object that can render a status bar, displaying the entities current hp.
    """
    def __init__(self, hp, defense, damage_filters=None):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.damage_filters = []
        if damage_filters:
            for filter in damage_filters:
                self.damage_filters.append(filter)
        self.status_bar = StatusBar(
            total_width=PANEL_CONFIG['bar_width'],
            bar_colors=STATUS_BAR_COLORS['hp_bar'])

    def harm(self, amount, element):
        """Apply damage from an element.

        It is not neccesarrly that the entity take all of the damage.  The
        entity may have equipment or resistances that grant them filters for
        incomping damage.
        """
        for filter in self.damage_filters:
            amount = filter.filter_damage(amount, element)
        self.hp -= amount
        results = []
        if self.hp <= 0:
            results.append({ResultTypes.DEAD_ENTITY: self.owner})
        return results

    def heal(self, amount):
        """Restore some amount of hp."""
        self.hp += min(amount, self.max_hp - self.hp)

    def render_status_bar(self, panel, x, y):
        self.status_bar.render(
            panel, x, y, 
            name=self.owner.name + ' HP',
            maximum=self.max_hp,
            value=self.hp)


class NullHarmable:

    def harm(self, amount, element):
        return []

    def heal(self, amount, element):
        return []

    def render_status_bar(self, panel, x, y):
        pass

    def __bool__(self):
        """Prevent entities with this component from showing up in searches for
        harmable entities.
        """
        return False
