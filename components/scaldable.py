from messages import Message
from etc.enum import ResultTypes, Elements
from etc.game_config import SCALD_BASE_DAMAGE


class AliveScaldable:
    """A living creature takes water elemental damage from being scalded."""
    def scald(self, game_map):
        return [{ResultTypes.DAMAGE: (
            self.owner, None, SCALD_BASE_DAMAGE, [Elements.WATER])}]


class FireBloatScaldable:
    """Steam immediately kills a fire bloat without causing a fireblast."""
    def scald(self, game_map):
            return [{ResultTypes.DEAD_ENTITY: self.owner}]
