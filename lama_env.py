from typing import Callable

import numpy as np
from PDDL import PDDL_Parser
from action import Action

from itertools import combinations, permutations
import copy

State = "frozenset[tuple]"


def sublist_in_list(sublist, list):
    c = 0
    res = False
    for i in sublist:
        if i in list:
            c += 1
    if c == len(sublist):
        res = True
    return res


def sublist_not_in_list(sublist, list):  # none of elements in sublist are in list
    res = True
    for i in sublist:
        if i in list:
            res = False
    return res


def replace_names_by_values_in_predicate(param_names, params_values, predicate):
    new_predicate = tuple(
        [predicate[0]]
        + [
            params_values[param_names.index(predicate[i])]
            for i in range(1, len(predicate))
        ]
    )
    return new_predicate


def get_next_state(state, operation, applicable_parameters):
    successor_states = []
    param_names = [param[0] for param in operation.parameters]
    for parameters in applicable_parameters:
        new_state = copy.deepcopy(state)
        # effects with the names of the parameters replaced :
        add_effects = [
            replace_names_by_values_in_predicate(param_names, parameters, effect)
            for effect in list(operation.add_effects)
        ]
        del_effects = [
            replace_names_by_values_in_predicate(param_names, parameters, effect)
            for effect in list(operation.del_effects)
        ]
        new_state = new_state.difference(del_effects)
        new_state = new_state.union(add_effects)
        successor_states.append(new_state)
    return successor_states


class LamaEnv:
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

    def create_successors_generators(self):
        return

    def is_applicable(self, state, operation):
        nb_parameters = len(operation.parameters)
        applicable_parameters = []
        param_names = [param[0] for param in operation.parameters]
        for list_parameters in list(combinations(self.variables, nb_parameters)):
            for parameters in list(permutations(list_parameters)):
                # preconditions with the names of the parameters replaced !
                positive_preconditions = [
                    replace_names_by_values_in_predicate(
                        param_names, parameters, precond
                    )
                    for precond in list(operation.positive_preconditions)
                ]
                negative_preconditions = [
                    replace_names_by_values_in_predicate(
                        param_names, parameters, precond
                    )
                    for precond in list(operation.negative_preconditions)
                ]
                if sublist_in_list(
                    positive_preconditions, state
                ) and sublist_not_in_list(negative_preconditions, state):
                    applicable_parameters.append(parameters)

        return len(applicable_parameters) > 0, applicable_parameters

    def get_successors(self, state: State, method: str = "naive") -> "list[State]":
        if method == "naive":
            applicable_operations = []
            applicable_corresponding_parameters = {}
            successors = []
            for operation in self.operations:
                is_applicable, applicable_parameters = self.is_applicable(
                    state, operation
                )
                if is_applicable:
                    applicable_operations.append(operation)
                    if operation.name not in applicable_corresponding_parameters:
                        applicable_corresponding_parameters[
                            operation.name
                        ] = applicable_parameters
                    else:
                        applicable_corresponding_parameters[
                            operation.name
                        ] += applicable_parameters
                    successor_states = get_next_state(
                        state, operation, applicable_parameters
                    )
                    successors += successor_states
            return (
                successors,
                applicable_operations,
                applicable_corresponding_parameters,
            )
        elif method == "successor_generator":
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


if __name__ == "__main__":
    parser = PDDL_Parser()

    domain = "./instances/groupe2/domain.pddl"
    problem = "./instances/groupe2/problem0.pddl"
    parser.parse_domain(domain)
    parser.parse_problem(problem)
    heuristic = len
    lama = LamaEnv(parser, heuristic)

    # test get_successors method :

    successors, applicable_operations, applicable_parameters = lama.get_successors(
        lama.initial_state
    )

    print(len(successors))

    for successor in successors:
        print([list(i) for i in successor if not i[0] == "adjacent"])
