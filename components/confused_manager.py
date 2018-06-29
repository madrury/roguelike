from components.movable import ConfusedMovable
from etc.config import PANEL_CONFIG
from etc.colors import STATUS_BAR_COLORS
from status_bar import StatusBar


class PlayerConfusedManager:
    """Manage swapping out the movable component on the player when the player
    becomes confused or recovers from being confused.

    When activated, this swaps the usual movable component with an instance of
    the ConfusedMovable component.  It then recieves a tick message every turn,
    which it tracks in an internal counter.  When the counter reaches a
    threshold, the object swaps back in the usual component and then destroys
    itself.
    """
    def __init__(self, n_confused_turns=20):
        self.n_turns = 0
        self.old_movable = None
        self.n_confused_turns = n_confused_turns
        self.status_bar = StatusBar(
            total_width=PANEL_CONFIG['bar_width'],
            bar_colors=STATUS_BAR_COLORS['confused_bar'])

    def attach(self, player):
        self.old_movable = player.movable
        player.add_component(ConfusedMovable(), "movable")
        player.add_component(self, "confused_manager")

    def tick(self):
        self.n_turns += 1
        if self.n_turns >= self.n_confused_turns:
            self.owner.add_component(self.old_movable, "movable")
            self.owner.confused_manager = None

    def render_status_bar(self, panel, x, y):
        self.status_bar.render(
            panel, x, y, 
            name='Confused',
            maximum=self.n_confused_turns,
            value=(self.n_confused_turns - self.n_turns))
