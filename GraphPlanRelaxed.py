import networkx as nx
import numpy as np
from itertools import compress
from functools import reduce

class GraphPlanRelaxed():
    def __init__(self, task):
        self.initial_state = task.initial_state
        self.goal = task.goals
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(self.initial_state)
        self.possible_operators = task.operators
        self.clean_operators()
    
    def expand(self):
        state = frozenset(self.graph.nodes)
        node_added = 0
        for operator in self.possible_operators:
            if operator.preconditions.issubset(state):
                add_effects = operator.add_effects
                node_added+=len(add_effects-self.graph.nodes)
                self.graph.add_nodes_from(add_effects-self.graph.nodes)
                self.graph.add_node(operator)
                self.graph.add_edges_from(zip(operator.preconditions, len(operator.preconditions)*[operator]))
                self.graph.add_edges_from(zip(len(add_effects)*[operator], add_effects))
        self.clean_operators()
        if self.goal.issubset(self.graph.nodes):
            return True, node_added
        return False, node_added

    def expand_until_goal(self):
        if self.goal.issubset(self.graph.nodes):
            return True
        complete = False
        node_added = len(self.graph.nodes)
        while (not complete) and (node_added>0):
            complete, node_added = self.expand()
        if complete:
            return True
        else:
            return False

    def clean_operators(self):
        state = frozenset(self.graph.nodes)
        effect_operators = list(map(lambda operator: operator.add_effects-state, self.possible_operators))
        keep = []
        for i, effects in enumerate(effect_operators):
            keep.append(self.check_subset(i, effects, effect_operators))

        self.possible_operators = list(compress(self.possible_operators, keep))
    
    def back_from_goal(self):
        goals = self.goal - self.initial_state
        self.pred = self.graph.pred
        actions = frozenset()
        i=0
        while len(goals)>0:
            new_goals, set_actions = self.select_action_backward(goals)
            actions = actions.union(set_actions)
            goals = new_goals - self.initial_state
            i+=1
        return actions
    
    def select_action_backward(self, goals):
        set_actions = frozenset()
        complete_goals = frozenset()
        for goal in goals:
            if not (goal in complete_goals):
                actions = list(self.pred[goal].keys())
                index = np.argmax(list(map(lambda action: len(action.add_effects.intersection(goals-complete_goals)), actions)))
                action = actions[index]
                complete_goals = complete_goals.union(action.add_effects)
                set_actions = set_actions.union(frozenset([action]))


        new_goals = reduce(lambda x,y: x.union(y), map(lambda action: frozenset(self.pred[action].keys()), set_actions)) - complete_goals
        return new_goals, set_actions
        

    def check_subset(self, i, effects, list_set):
        for j, effect_compare in enumerate(list_set):
            if effects==effect_compare:
                if j<i:
                    return False
            elif effects.issubset(effect_compare):
                return False
                break
        return True
    
    def get_FF_heuristic(self):
        self.expand_until_goal()
        actions = self.back_from_goal()
        return actions, len(actions)