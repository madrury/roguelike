from etc.enum import ResultTypes, Elements
from etc.config import PANEL_CONFIG
from etc.colors import STATUS_BAR_COLORS
from status_bar import StatusBar


class Swimmable:

    def __init__(self, stamina):
        self.max_stamina = stamina
        self.stamina = stamina
        self.status_bar = StatusBar(
            total_width=PANEL_CONFIG['bar_width'],
            bar_colors=STATUS_BAR_COLORS['swim_bar'])

    def swim(self):
        results = []
        if self.stamina > 0:
            results.append({ResultTypes.CHANGE_SWIM_STAMINA: (self.owner, -1)})
        if self.stamina <= 0:
            results.append({ResultTypes.DAMAGE: (self.owner, 5, [elements.WATER])})
        return results

    def rest(self):
        results = []
        results.append({ResultTypes.CHANGE_SWIM_STAMINA: (self.owner, 1)})
        return results

    def change_stamina(self, change):
        if self.stamina < 0:
            self.stamina = 0
        else:
            self.stamina = min(max(0, self.stamina + change), self.max_stamina)

    def render_status_bar(self, panel, x, y):
        self.status_bar.render(
            panel, x, y, 
            name='Swim Stamina',
            maximum=self.max_stamina,
            value=self.stamina)
