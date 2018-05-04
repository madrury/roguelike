from messages import Message
from etc.enum import ResultTypes
from etc.colors import COLORS
from spawnable.various import Fire


class GrassBurnable:

    def burn(self):
        message = Message("The grass burns away.", COLORS["orange"])
        fire = Fire.maybe_make(self.owner.x, self.owner.y) 
        if fire:
            return [{
                ResultTypes.MESSAGE: message,
                ResultTypes.REMOVE_ENTITY: self.owner,
                ResultTypes.ADD_ENTITY: fire}] 
        else:
            return [{
                ResultTypes.MESSAGE: message,
                ResultTypes.REMOVE_ENTITY: self.owner}]
