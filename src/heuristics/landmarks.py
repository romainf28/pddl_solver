from collections import defaultdict
import copy


def _get_relaxed_task(task):
    """
    Removes the delete effects of the operators
    """
    relaxed_task = copy.deepcopy(task)
    for op in relaxed_task.operators:
        op.del_effects = set()
    return relaxed_task


def get_landmarks(task):
    """Returns a set of landmarks.
    """
    # remove del effects of operators
    task = _get_relaxed_task(task)
    landmarks = set(task.goals)
    possible_landmarks = task.facts - task.goals

    for fact in possible_landmarks:
        current_state = task.initial_state
        # goal is reached is all of the goal facts are in the current state
        is_goal_reached = task.goals.issubset(current_state)

        while not is_goal_reached:
            old_state = current_state

            for op in task.operators:
                # try to apply an operator to the current state
                if op.applicable(current_state) and fact not in op.add_effects:
                    current_state = op.apply(current_state)
                    if task.goals.issubset(current_state):
                        break
            # if there is no operators which can change the state without adding the fact,
            # this fact is necassry to reach the goal
            if old_state == current_state and not task.goals.issubset(current_state):
                landmarks.add(fact)
                break

            is_goal_reached = task.goals.issubset(current_state)
    return landmarks


def get_landmark_costs(task, landmarks):
    """
    Calculate cost of landmarks following the cost partitionning
    heuristic for landmarks
    """
    op_to_land = defaultdict(set)

    # for each operator, get the landmarks in its add effects
    for operator in task.operators:
        for landmark in landmarks:
            if landmark in operator.add_effects:
                op_to_land[operator].add(landmark)
    min_cost = defaultdict(lambda: float("inf"))

    for operator, landmarks in op_to_land.items():
        nb_landmarks = len(landmarks)
        for landmark in landmarks:
            min_cost[landmark] = min(
                min_cost[landmark], 1 / nb_landmarks)
    return min_cost


class LandmarkHeuristic:
    def __init__(self, task):
        self.task = task

        self.landmarks = get_landmarks(task)
        assert self.task.goals.issubset(self.landmarks)
        self.costs = get_landmark_costs(task, self.landmarks)

    def __call__(self, node):
        """Returns the heuristic value for a given node"""
        if node.parent is None:
            # At first, only the initial facts are achieved
            node.not_reached = self.landmarks - self.task.initial_state
        else:
            # A new node reaches the facts in its add_effects
            node.not_reached = node.parent.not_reached - node.action.add_effects
        # The goal facts should be unreached if they are not true
        # in the current state, even if they have been reached before
        not_reached = node.not_reached | (self.task.goals - node.state)

        h_val = sum(self.costs[landmark] for landmark in not_reached)
        return h_val
