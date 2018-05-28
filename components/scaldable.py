from messages import Message
from etc.enum import ResultTypes, Elements


class AliveScaldable:
    """A living creature takes water elemental damage from being scalded."""
    def scald(self, game_map):
        # TODO: Move to config.py
        return [{ResultTypes.DAMAGE: (self.owner, None, 5, [Elements.WATER])}]


class FireBloatScaldable:
    """Steam immediately kills a fire bloat without causing a fireblast."""
    def scald(self, game_map):
            return [{ResultTypes.DEAD_ENTITY: self.owner}]
