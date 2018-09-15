from etc.enum import TreeStates

from components.behaviour_trees.root import Node


class Sequence(Node):
    """Tick childeren in sequence we encounter a failure.  If no failure is
    encountered, propogate the results of the final child.
    """
    def __init__(self, *children):
        for child in children:
            child.parent = self
        self.children = children

    def tick(self, owner, game_map):
        for child in self.children:
            state, results = child.tick(owner, game_map)
            if state == TreeStates.FAILURE:
                return state, results
        return state, results
        

class Selection(Node):
    """Tick chideren in sequence until success and propogate the results of
    that success.  If no success is encuntered, propogate failure.
    """
    def __init__(self, *children):
        for child in children:
            child.parent = self
        self.children = children

    def tick(self, owner, game_map):
        for child in self.children:
            state, results = child.tick(owner, game_map)
            if state == TreeStates.SUCCESS:
                return state, results
        return TreeStates.FAILURE, []


class Negate(Node):
    """Tick a single child and return negation of the resulting state."""
    def __init__(self, child):
        child.parent = self
        self.child = child

    def tick(self, owner, game_map):
        state, results = self.child.tick(owner, game_map)
        if state == TreeStates.SUCCESS:
            return TreeStates.FAILURE, results
        elif state == TreeStates.FAILURE:
            return TreeStates.SUCCESS, results
        return state, results
