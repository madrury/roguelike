class Root:
    """The root node of a behaviour tree holds the namespace for the entire
    operation.
    """
    def __init__(self, namespace=None):
        if namespace is None:
            namespace = {}
        self.namespace = namespace
        

class Node:
    """A mixin for all the nodes in a behaviour tree *except* the root node.
    Delegates namespace lookups to parent nodes.
    """
    @property
    def namespace(self):
        return self.parent.namespace
