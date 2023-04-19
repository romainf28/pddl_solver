class SearchNode:
    """
    Each search node has a parent node and contains informations about 
    - the state 
    - the actions to apply to reach the node
    - the path length to reach the node
    """

    def __init__(self, state, parent, action, g):
        """
        Arguments

        - state: The state
        - parent: The parent node
        - action: The action which led to the state
        - g : The path length to reach the node
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.g = g

    def extract_solution(self):
        """
        Returns the list of actions that were applied from the initial node to
        the goal node.
        """
        sol = []
        while self.parent is not None:
            sol.append(self.action)
            self = self.parent
        sol.reverse()
        return sol


def make_root_node(initial_state):
    """
    Construct the root node.
    """
    return SearchNode(initial_state, None, None, 0)


def make_child_node(parent, action, state):
    """
    Construct a new search node containing the state and the applied action.
    """
    return SearchNode(state, parent, action, parent.g + 1)
