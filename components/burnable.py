from messages import Message
from etc.enum import ResultTypes
from etc.colors import COLORS
from spawnable.various import Fire


class GrassBurnable:

    def burn(self):
        fire = Fire.maybe_make(self.owner.x, self.owner.y, p=0.8) 
        if fire:
            return [{
                ResultTypes.REMOVE_ENTITY: self.owner,
                ResultTypes.ADD_ENTITY: fire}] 
        else:
            return [{
                ResultTypes.REMOVE_ENTITY: self.owner}]
