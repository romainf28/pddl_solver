import networkx as nx
import numpy as np
from itertools import compress
from functools import reduce


class GraphPlanRelaxed():
    """
    A class permitting to create a graph plan relaxed from a given grounded task.
    It is used to compute FF heuristic.
    """

    def __init__(self, task):
        # initial state from the task (can be modified if you want to do heuristic algo)
        self.initial_state = task.initial_state

        # goal of the task
        self.goal = task.goals

        # initialization of a directionnal graph
        self.graph = nx.DiGraph()

        # add initial state in the graph
        self.graph.add_nodes_from(self.initial_state)

        # list of all possible and useful operators from the state of the graph
        self.possible_operators = task.operators  # initialization with all operators
        self.clean_operators()  # cleaning to keep the desired one

    def expand(self):
        """
        Expand the graph from his current state (add action and literal to go to the next state)
        Return: True if all goals are in the graph, False otherwise
                nodes_added : The number of literals added in the graph
        """
        state = frozenset(
            self.graph.nodes)  # current state is all the element in the graph (we just use literal)
        nodes_added = 0
        # loop over possible usefull operators
        for operator in self.possible_operators:
            # check if the action is possible
            if operator.pos_preconditions.issubset(state) and operator.neg_preconditions.isdisjoint(state):
                add_effects = operator.add_effects
                # add the number of effects that are not already in the graph
                nodes_added += len(add_effects-self.graph.nodes)
                self.graph.add_nodes_from(add_effects-self.graph.nodes)
                # add the action in th graph
                self.graph.add_node(operator)
                # create edges between each preconditions and the action
                self.graph.add_edges_from(
                    zip(operator.pos_preconditions, len(operator.pos_preconditions)*[operator]))
                # create edges between the action and each effect of the action
                self.graph.add_edges_from(
                    zip(len(add_effects)*[operator], add_effects))

        self.clean_operators()  # keep only usefull actions

        if self.goal.issubset(self.graph.nodes):  # check if the goal is attempted
            return True, nodes_added
        return False, nodes_added

    def expand_until_goal(self):
        """
        Expand the graph until the goal is attempted
        Return: True goal attempted, False goal is not possible
        """
        if self.goal.issubset(self.graph.nodes):  # check if the goal is already attempted
            return True
        complete = False
        node_added = len(self.graph.nodes)
        # expand the graph until goal is attempted or no more nodes are added
        while (not complete) and (node_added > 0):
            complete, node_added = self.expand()

        return complete

    def clean_operators(self):
        """
        Keep only operators that create new usefull literals 
        (if two create the same literals, the first one is added)
        """
        state = frozenset(self.graph.nodes)  # all states in the graph
        # list of the effects of operators that are not already in the graph
        effect_operators = list(
            map(lambda operator: operator.add_effects-state, self.possible_operators))
        keep = []
        for i, effects in enumerate(effect_operators):
            # check if the usefull effects of the opertor is a subset of another one (if same keep first)
            keep.append(self.check_subset(i, effects, effect_operators))

        # selection of the desired operators
        self.possible_operators = list(compress(self.possible_operators, keep))

    def check_subset(self, i, effects, list_set):
        """
        Check if the set of effects is a subset of one set of list_set (if same keep first)
        Return True if it is not the case, false otherwise.
        """
        for j, effect_compare in enumerate(list_set):
            if effects == effect_compare:
                if j < i:
                    return False
            elif effects.issubset(effect_compare):
                return False
        return True

    def back_from_goal(self):
        """
        Road back from goal to initial state
        """
        goals = self.goal - self.initial_state  # goals not attempted
        self.pred = self.graph.pred
        actions = frozenset()  # actions done
        i = 0
        while len(goals) > 0:
            # print(i, "===================================")
            new_goals, set_actions = self.select_actions_backward(goals)
            actions = actions.union(set_actions)  # add new actions
            goals = new_goals - self.initial_state  # goals not attempted
            i += 1
        return actions

    def select_actions_backward(self, goals):
        """
        Step backward to go to the initial state
        """
        set_actions = frozenset()
        complete_goals = frozenset()
        # iterate throw goals
        for goal in goals:
            if not (goal in complete_goals):  # check if the goal is not already done
                # possible actions to attempt the goals
                actions = list(self.pred[goal].keys())
                # selection of the action completing the highest number of goals not already done
                index = np.argmax(list(map(lambda action: len(
                    action.add_effects.intersection(goals-complete_goals)), actions)))
                action = actions[index]
                # print("Goal : ", goal, "Actions : ", action)
                # add effects of the action to the completed goals
                complete_goals = complete_goals.union(action.add_effects)
                # add action to the set of action
                set_actions = set_actions.union(frozenset([action]))
        # preconditions of the actions needed - the ones already done at this stage
        new_goals = reduce(lambda x, y: x.union(y), map(lambda action: frozenset(
            self.pred[action].keys()), set_actions)) - complete_goals
        return new_goals, set_actions

    def get_FF_heuristic(self):
        """
        Get FF heuristic from the given task
        """
        self.expand_until_goal()  # create graph
        actions = self.back_from_goal()  # set of actions to go to the goal
        return actions, len(actions)
