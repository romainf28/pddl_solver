from itertools import chain
from typing import Callable, Iterable, List, Optional, Set, Tuple
from collections import deque
from networkx import DiGraph

import numpy as np
from PDDL import PDDL_Parser
from action import Action

from itertools import combinations, permutations
import copy
from lama_types import Fact, Landmark, Ordering, State

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
        # Regular and preferred open lists for each heuristic
        self.reg: dict[str, deque[State]] = {LamaEnv.FF: deque(), LamaEnv.LM: deque()}
        self.pref: dict[str, deque[State]] = {LamaEnv.FF: deque(), LamaEnv.LM: deque()}

        # Numerical priority for each queue
        self.priority: dict[deque[State], int] = {
            self.reg[LamaEnv.FF]: 0,
            self.reg[LamaEnv.LM]: 0,
            self.pref[LamaEnv.FF]: 0,
            self.pref[LamaEnv.LM]: 0,
        }
        # Best heuristic value seen so far for each heuristic
        self.best_seen_value = {LamaEnv.FF: np.inf, LamaEnv.LM: np.inf}

        # Landmarks variables
        self.LG: DiGraph[Fact] = DiGraph()  # Landmark graph
        self.queue: deque[Landmark] = deque()  # Landmarks to be back-chained from

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

    def execute_heuristic(self, state, name: str) -> Tuple[int, Action]:
        if name == LamaEnv.FF:
            return self.FastForward(state)

        if name == LamaEnv.LM:
            return self.Landmarks(state)

        raise Exception("Unknown heuristic")

    def FastForward(self, state: State) -> Tuple[int, List[Action]]:
        return 0, self.operations

    def Landmarks(self, state: State) -> Tuple[int, List[Action]]:
        return 0, self.operations

    def get_successors(self, state: State) -> List[State]:
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

        if progress:  # Boost preferred-operator queues
            self.priority[self.pref[LamaEnv.FF]] += 1000
            self.priority[self.pref[LamaEnv.LM]] += 1000

        successors = self.get_successors(state)
        for successor in successors:
            for h in heuristics:
                self.reg[h].append(successor)  # Deferred evaluation
                transition = self.get_operator(state, successor)
                if transition in preferred_ops[h]:
                    self.pref[LamaEnv.FF].append(successor)
                    self.pref[LamaEnv.LM].append(successor)

    def satisfies_goal(self, state: State):
        return self.positive_goals.intersection(
            state
        ) == self.positive_goals and not self.negative_goals.intersection(state)

    def greedy_BFS_Lama(self) -> Tuple[int, List[State]]:
        self.init_variables()  # Initialize FF and landmark heuristics
        closed_list = []
        current_state = self.initial_state

        while True:
            if current_state not in closed_list:
                if self.satisfies_goal(current_state):
                    return 1, closed_list
                closed_list.append(current_state)
                self.expand_state(current_state)

            if (
                sum([len(queue) for queue in self.priority.keys()]) == 0
            ):  # No plan exists
                return 0, []  # failure

            sorted_queues: list[deque] = sorted(
                self.priority.keys(), key=self.priority.get
            )
            i = 0
            queue = None
            while queue is None:
                if len(sorted_queues[i]) > 0:
                    queue = sorted_queues[i]
                i += 1

            self.priority[queue] -= 1
            current_state = queue.popleft()  # Get lowest-valued state from queue q

    def add_landmark_and_ordering(self, landmark: Landmark, ordering: Ordering):
        if landmark.is_fact:  # Prefer fact landmarks
            fact = landmark.fact
            disjonctive_landmarks = [
                graph_landmark
                for graph_landmark in self.LG.nodes
                if fact in graph_landmark.facts
            ]
            # Remove disjunctive landmarks
            self.LG.remove_nodes_from(disjonctive_landmarks)

        if (
            landmark.is_nfact
        ):  # Prefer fact landmarks: we are checking for the negative facts
            nfact = landmark.nfact
            disjonctive_landmarks = [
                graph_landmark
                for graph_landmark in self.LG.nodes
                if nfact in graph_landmark.nfacts
            ]
            # Remove disjunctive landmarks
            self.LG.remove_nodes_from(disjonctive_landmarks)

        for graph_landmark in self.LG.nodes:
            # Abort on overlap with existing landmark
            if not landmark.variables.isdisjoint(graph_landmark.variables):
                return

        if not self.LG.has_node(landmark):  # Add new landmark to graph
            self.LG.add_node(landmark)
            self.queue.append(landmark)

        self.LG.add_edge(landmark, ordering[1])  # Add new ordering to graph

    def get_restricted_relaxed_plan_graph(self, landmark: Landmark) -> DiGraph:
        pass

    def get_landmarks_iterator(
        self, facts: Set[Fact], nfacts: Set[Fact]
    ) -> Iterable[Landmark]:
        return chain(
            (Landmark({fact}, set()) for fact in facts),
            (Landmark(set(), {nfact}) for nfact in nfacts),
        )

    def get_shared_preconditions(self, RRPG: DiGraph) -> Iterable[Landmark]:
        preconditions: Optional[Set[Fact]] = None
        npreconditions: Optional[Set[Fact]] = None
        for operation in RRPG.nodes:
            if preconditions is None:
                preconditions = operation.positive_preconditions
            else:
                preconditions = preconditions.intersection(
                    operation.positive_preconditions
                )
            if npreconditions is None:
                npreconditions = npreconditions.negative_preconditions
            else:
                npreconditions = npreconditions.intersection(
                    operation.negative_preconditions
                )

        return self.get_landmarks_iterator(preconditions, npreconditions)

    def identify_landmarks(self):
        initial_landmarks = self.get_landmarks_iterator(
            self.positive_goals, self.negative_goals
        )
        # Landmark graph starts with all goals, no orderings
        self.LG.add_nodes_from(initial_landmarks)

        self.queue.extend(initial_landmarks)
        # further_orderings = []  # Additional orderings voir plus tard pour efficiency
        while len(self.queue) > 0:
            landmark = self.queue.popleft()

            if not landmark.is_satisfied_in_state(self.initial_state):
                RRPG = self.get_restricted_relaxed_plan_graph(landmark)

            for precond in self.get_shared_preconditions(RRPG):
                if not precond.is_satisfied_in_state(self.initial_state):
                    self.add_landmark_and_ordering(precond, (precond, landmark))

            # further_orderings.append() # Voir cette ligne plus tard, souci d'efficiency


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
