from messages import Message
from etc.enum import ResultTypes

class Inventory:

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def __iter__(self):
        yield from iter(self.items)

    def pickup(self, item):
        results = []
        if len(self.items) >= self.capacity:
            results.append({
                ResultTypes.END_TURN: True,
                ResultTypes.MESSAGE: Message(
                    f'{self.owner.name} cannot carry any more items.')})
        else:
            results.append({
                ResultTypes.END_TURN: True,
                ResultTypes.ITEM_ADDED: item,
                ResultTypes.MESSAGE: Message(
                    f'{self.owner.name} picks up the {item.name}.')})
        return results

    def drop(self, item):
        results = []
        if item.equipable and item.equipable.equipped:
            message = Message(
                f'{self.owner.name} cannot drop {item.name}, as it is currently equipped.')
            results.append({
                ResultTypes.END_TURN: True,
                ResultTypes.MESSAGE: message})
        else:
            message = Message(f'{self.owner.name} dropped the {item.name}')
            results.append({
                ResultTypes.END_TURN: True,
                ResultTypes.ITEM_DROPPED: item,
                ResultTypes.MESSAGE: message})
        return results

    def add(self, item):
        self.items.append(item)

    def extend(self, items):
        self.items.extend(items)

    def remove(self, item):
        self.items.remove(item)
