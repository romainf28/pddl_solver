import search_node
import heapq


def ordered_node_weighted_astar(weight):
    """
    Creates a tuple with the node and an order for weighted A* search (order = g+weight*h).
    Returns a function which takes as arguments :
    -  node : The node 
    - h : The heuristic value
    - node_preference : a value which represents preference for nodes inserted first
    if the oredrings are equal.
    """
    return lambda node, h, node_preference: (
        node.g + weight * h,
        h,
        node_preference,
        node,
    )


def weighted_astar_search(
    task, heuristic, weight=5
):
    """
    Searches for a plan using weighted A* search.
    Arguments 
    - task : the PDDL task
    - heuristic : A heuristic to estimate the number of steps from a node to the goal
    """
    open = []
    state_cost = {task.initial_state: 0}
    node_preference = 0

    # construct root node
    root = search_node.make_root_node(task.initial_state)
    init_h_val = heuristic(root)
    # create new search node and ordering
    heapq.heappush(open, ordered_node_weighted_astar(weight)(
        root, init_h_val, node_preference))

    min_h = float("inf")
    count = 0
    nb_expansions = 0

    while open:
        (f, h_val, preference, node) = heapq.heappop(open)
        if h_val < min_h:
            min_h = h_val
            print("Found new best h value ({}) after {} expansions".format(min_h, count))

        state = node.state
        # expand the node if its cost g is the min cost for this state.
        # Else, a cheaper path has been found
        if state_cost[state] == node.g:
            nb_expansions += 1

            if task.is_goal_reached(state):
                print("Goal reached, extracting solution ...")
                return node.extract_solution()
            plan = None

            for op, next_state in task.get_next_states(state):

                next_node = search_node.make_child_node(
                    node, op, next_state)
                h_val = heuristic(next_node)
                if h_val == float("inf"):
                    # can't reach the goal
                    continue
                old_next_g = state_cost.get(next_state, float("inf"))
                if next_node.g < old_next_g:
                    # this means that we either visited next state before
                    # or found a cheaper path to this sate
                    node_preference += 1
                    heapq.heappush(open, ordered_node_weighted_astar(weight)(
                        next_node, h_val, node_preference))
                    state_cost[next_state] = next_node.g

        count += 1
    print("Task unsolvable : no operators left")
    return None
