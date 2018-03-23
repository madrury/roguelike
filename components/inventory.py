from game_messages import Message

class Inventory:

    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def pickup_item(self, item):
        results = []
        if len(self.items) >= self.capacity:
            results.append({
                'message': Message('You cannot carry any more items.')})
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}.'.format(item.name))})
        return results