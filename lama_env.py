from typing import Callable

import numpy as np
from PDDL import PDDL_Parser
from action import Action

State = "frozenset[tuple]"


class LamaEnv():

    def __init__(self, parser: PDDL_Parser, heuristic: Callable):
        self.parser = parser

        self.variables = parser.objects["object"]
        self.initial_state = parser.state

        self.positive_goals = parser.positive_goals
        self.negative_goals = parser.negative_goals

        self.operations = parser.actions
        self.heuristic = heuristic

        self.FF: dict[frozenset[tuple], int] = {}
        self.LM: dict[frozenset[tuple], int] = {}

        self.regFF: list[int] = []
        self.prefFF: list[int] = []
        self.regLM: list[int] = []
        self.prefLM: list[int] = []

        self.priority: dict[list[int], int] = {}
        self.best_seen_value = {self.FastForward: np.inf, self.Lama: np.inf}

    
    def FastForward(self, state: State) -> "tuple[int, Action]":
        return 0, self.operations[0]

    def Lama(self, state: State) -> "tuple[int, Action]":
        return 0, self.operations[0]
    
    def get_successors(self, state: State) -> "list[State]":
        return []


    def expand_state(self, state: State):
        progress = False

        for h in [self.FastForward, self.Lama]:
            value, preferred_ops = h(state)
            if value < self.best_seen_value[h]:
                progress = True
                self.best_seen_value[h] = value

        if progress:
            self.priority[self.prefFF] += 1000
            self.priority[self.prefLM] += 1000

