from game_messages import Message
from etc.enum import ResultTypes

class Inventory:

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def pickup(self, item):
        results = []
        if len(self.items) >= self.capacity:
            results.append({
                ResultTypes.MESSAGE: Message('You cannot carry any more items.')})
        else:
            results.append({
                ResultTypes.ITEM_ADDED: item,
                ResultTypes.MESSAGE: Message('You pick up the {0}.'.format(item.name))})
        return results

    def drop(self, item):
        results = []
        message = Message(f'You dropped the {item.name}')
        results.append({
            ResultTypes.ITEM_DROPPED: item,
            ResultTypes.MESSAGE: message})
        return results

    def add(self, item):
        self.items.append(item)

    def extend(self, items):
        self.items.extend(items)

    def remove(self, item):
        self.items.remove(item)
