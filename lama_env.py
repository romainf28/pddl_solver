from typing import Callable
from collections import deque
from networkx import Graph

import numpy as np
from PDDL import PDDL_Parser
from action import Action

State = "frozenset[tuple]"


class LamaEnv():

    LM = "LM"
    FF = "FF"

    def __init__(self, parser: PDDL_Parser, action_cost: Callable):
        self.parser = parser

        self.variables = parser.objects["object"]
        self.initial_state = parser.state

        self.positive_goals = parser.positive_goals
        self.negative_goals = parser.negative_goals

        self.operations = parser.actions
        self.action_cost = action_cost
        self.init_variables()

    def init_variables(self):
        self.FF: dict[frozenset[tuple], int] = {}
        self.LM: dict[frozenset[tuple], int] = {}

        self.reg: dict[str, deque[State]] = {LamaEnv.FF: deque(), LamaEnv.LM: deque()}
        self.pref: dict[str, deque[State]] = {LamaEnv.FF: deque(), LamaEnv.LM: deque()}

        self.priority: dict[deque[State], int] = {
            self.reg[LamaEnv.FF]: 0,
            self.reg[LamaEnv.LM]: 0,
            self.pref[LamaEnv.FF]: 0,
            self.pref[LamaEnv.LM]: 0,
        }
        self.best_seen_value = {LamaEnv.FF: np.inf, LamaEnv.LM: np.inf}
        
        # Landmarks variables
        LG = Graph()
        queue: deque()

    def execute_heuristic(self, state, name: str) -> "tuple[int, Action]":
        if name == LamaEnv.FF:
            return self.FastForward(state)
        
        if name == LamaEnv.LM:
            return self.Landmarks(state)
        
        raise Exception("Unknown heuristic")
    
    def FastForward(self, state: State) -> "tuple[int, list[Action]]":
        return 0, self.operations

    def Landmarks(self, state: State) -> "tuple[int, list[Action]]":
        return 0, self.operations
    
    def get_successors(self, state: State) -> "list[State]":
        return []
    
    def get_operator(self, state: State, successor: State) -> Action:
        return self.operations[0]

    def expand_state(self, state: State):
        progress = False
        heuristics = [LamaEnv.LM, LamaEnv.FF]
        preferred_ops: dict[str, list[Action]]

        for h in heuristics:
            value, preferred_ops[h] = h(state)
            if value < self.best_seen_value[h]:
                progress = True
                self.best_seen_value[h] = value

        if progress:
            self.priority[self.pref[LamaEnv.FF]] += 1000
            self.priority[self.pref[LamaEnv.LM]] += 1000

        successors = self.get_successors(state)
        for successor in successors:
            for h in heuristics:
                self.reg[h].append(successor)
                transition = self.get_operator(state, successor)
                if transition in preferred_ops[h]:
                    self.pref[LamaEnv.FF].append(successor)
                    self.pref[LamaEnv.LM].append(successor)

    def satisfies_goal(self, state: State):
        for positive in self.positive_goals:
            if positive not in state:
                return False
        for negative in self.negative_goals:
            if negative in state:
                return False
        return True

    def greedy_BFS_Lama(self) -> "tuple[int, list[State]]":
        self.init_variables()
        closed_list = []
        current_state = self.initial_state

        while True:
            if current_state not in closed_list:
                if self.satisfies_goal(current_state):
                    return 1, closed_list
                closed_list.append(current_state)
                self.expand_state(current_state)

            if sum([len(queue) for queue in self.priority.keys()]) == 0:
                return 0, [] # failure
            
            sorted_queues: list[deque] = sorted(self.priority.keys(), key=self.priority.get)
            i = 0
            queue = None
            while queue is None:
                if len(sorted_queues[i]) > 0:
                    queue = sorted_queues[i]
                i += 1

            self.priority[queue] -= 1
            current_state = queue.popleft()
            
            


