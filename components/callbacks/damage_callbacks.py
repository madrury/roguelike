from etc.enum import ResultTypes

class ReflectCallback:

    def execute(self, target, source, amount, elements):
        if source:
            return [{ResultTypes.DAMAGE: (source, target, amount, elements)}]
        else:
            return []
