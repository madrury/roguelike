from messages import Message
from etc.enum import ResultTypes, Elements
from etc.config import PANEL_CONFIG 
from etc.colors import STATUS_BAR_COLORS
from status_bar import StatusBar


class Harmable:

    def __init__(self, hp, defense, fire_modifier=0):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.fire_modifier = fire_modifier
        self.status_bar = StatusBar(
            total_width=PANEL_CONFIG['bar_width'],
            bar_colors=STATUS_BAR_COLORS['hp_bar'])

    def take_damage(self, amount, element):
        if element == Elements.FIRE:
            amount -= self.fire_modifier
        self.hp -= amount
        results = []
        if self.hp <= 0:
            results.append({ResultTypes.DEAD_ENTITY: self.owner})
        return results

    def render_status_bar(self, panel, x, y):
        self.status_bar.render(
            panel, x, y, 
            name=self.owner.name + ' HP',
            maximum=self.max_hp,
            value=self.hp)


class NullHarmable:

    def take_damage(self, amount, element):
        return []

    def render_status_bar(self, panel, x, y):
        pass

    def __bool__(self):
        """Prevent entities with this component from showing up in searches for
        harmable entities.
        """
        return False
