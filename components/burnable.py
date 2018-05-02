from messages import Message
from etc.enum import ResultTypes
from etc.colors import COLORS


class GrassBurnable:

    def burn(self):
        message = Message("The grass burns away.", COLORS["orange"])
        return [{
            ResultTypes.MESSAGE: message,
            ResultTypes.REMOVE_ENTITY: self.owner}]
