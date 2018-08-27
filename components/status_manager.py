from etc.config import BOTTOM_PANEL_CONFIG
from etc.game_config import (
    PLAYER_CONFUSED_DURATION, ENEMY_CONFUSED_DURATION,
    ENEMY_FROZEN_DURATION)
from etc.colors import STATUS_BAR_COLORS
from status_bar import StatusBar

import components.input_handler
import components.ai


class PlayerConfusedManager:
    """Manage swapping out the movable component on the player when the player
    becomes confused or recovers from being confused.

    When activated, this swaps the usual movable component with an instance of
    the ConfusedMovable component.  It then recieves a tick message every turn,
    which it tracks in an internal counter.  When the counter reaches a
    threshold, the object swaps back in the usual component and then destroys
    itself.
    """
    def __init__(self, n_confused_turns=PLAYER_CONFUSED_DURATION):
        self.n_turns = 0
        self.old_input_handler = None
        self.n_confused_turns = n_confused_turns
        self.status_bar = StatusBar(
            total_width=BOTTOM_PANEL_CONFIG['bar_width'],
            bar_colors=STATUS_BAR_COLORS['confused_bar'])

    def attach(self, player):
        self.old_input_handler = player.input_handler
        player.add_component(
            components.input_handler.PlayerConfusedInputHandler(), "input_handler")
        player.add_component(self, "status_manager")

    def remove(self):
        self.owner.add_component(self.old_input_handler, "input_handler")
        self.owner.status_manager = None

    def tick(self):
        self.n_turns += 1
        if self.n_turns >= self.n_confused_turns:
            self.remove()

    def render_status_bar(self, panel, x, y):
        self.status_bar.render(
            panel, x, y, 
            name='Confused',
            maximum=self.n_confused_turns,
            value=(self.n_confused_turns - self.n_turns))


class EnemyConfusedManager:
    """Manage swapping out the ai component on an enemy when it becomes
    confused or recovers from being confused.
    """
    def __init__(self, n_confused_turns=ENEMY_CONFUSED_DURATION):
        self.n_turns = 0
        self.old_ai = None
        self.n_confused_turns = n_confused_turns

    def attach(self, entity):
        self.old_ai = entity.ai
        entity.add_component(components.ai.ConfusedMonster(), "ai")
        entity.add_component(self, "status_manager")

    def remove(self):
        self.owner.add_component(self.old_ai, "ai")
        self.owner.status_manager = None

    def tick(self):
        self.n_turns += 1
        if self.n_turns >= self.n_confused_turns:
            self.remove()


class EnemyFrozenManager:
    """Manage swapping out the ai component on an enemy when it becomes
    frozen or recovers from being frozen.
    """
    def __init__(self, n_frozen_turns=ENEMY_FROZEN_DURATION):
        self.n_turns = 0
        self.old_ai = None
        self.n_frozen_turns = n_frozen_turns

    def attach(self, entity):
        self.old_ai = entity.ai
        entity.add_component(components.ai.FrozenMonster(), "ai")
        entity.add_component(self, "status_manager")

    def remove(self):
        self.owner.add_component(self.old_ai, "ai")
        self.owner.status_manager = None

    def tick(self):
        self.n_turns += 1
        if self.n_turns >= self.n_frozen_turns:
            self.remove()
