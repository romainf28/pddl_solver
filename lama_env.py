from itertools import chain
from typing import Callable, Iterable, List, Optional, Set, Tuple
from collections import deque
from networkx import DiGraph

import numpy as np
from grounder import Grounder
from pddlparser import PDDLParser
from domain import Action

from itertools import combinations, permutations
import copy
from lama_types import Fact, Landmark, LandmarkPlan, Ordering, State
from planning_task import Operator, PlanningTask


class LamaEnv:
    LM = "LM"
    FF = "FF"

    def __init__(self, planning_task: PlanningTask, action_cost: Callable):
        self.planning_task = planning_task

        self.facts = planning_task.facts
        self.initial_state = planning_task.initial_state

        self.goals = planning_task.goals

        self.operations = planning_task.operators
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
        self.accepted: dict[
            Tuple[State, LandmarkPlan], Set[Landmark]
        ] = {}  # Landmarks accepted in states evaluated so far

    def FastForward(self, state: State) -> Tuple[int, Action]:
        return 0, self.operations[0]

    def Lama(self, state: State) -> Tuple[int, Action]:
        return 0, self.operations[0]

    def create_successors_generators(self):
        return

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

        successors = self.planning_task.get_next_states(state)
        for successor in successors:
            for h in heuristics:
                self.reg[h].append(successor)  # Deferred evaluation
                transition = self.get_operator(state, successor)
                if transition in preferred_ops[h]:
                    self.pref[LamaEnv.FF].append(successor)
                    self.pref[LamaEnv.LM].append(successor)

    def greedy_BFS_Lama(self) -> Tuple[int, List[State]]:
        self.init_variables()  # Initialize FF and landmark heuristics
        closed_list = []
        current_state = self.initial_state

        while True:
            if current_state not in closed_list:
                if self.planning_task.is_goal_reached(current_state):
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
        a = Operator()
        a.neg_preconditions
        for operation in RRPG.nodes:
            if preconditions is None:
                preconditions = operation.pos_preconditions
            else:
                preconditions = preconditions.intersection(operation.pos_preconditions)
            if npreconditions is None:
                npreconditions = npreconditions.neg_preconditions
            else:
                npreconditions = npreconditions.intersection(
                    operation.neg_preconditions
                )

        return self.get_landmarks_iterator(preconditions, npreconditions)

    def identify_landmarks(self):
        initial_landmarks = self.get_landmarks_iterator(self.goals, {})
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

    def get_reached(
        self, state: State, accepted_landmarks: Set[Landmark]
    ) -> Set[Landmark]:
        return {
            landmark
            for landmark in self.LG.nodes
            if state.issubset(landmark.facts)
            and all(
                neighbour in accepted_landmarks
                for neighbour in self.LG.neighbors(landmark)
            )
        }

    def LM_count_heuristic(self, state: State, plan: LandmarkPlan):
        if len(plan) == 0:
            self.accepted[(state, plan)] = set(
                node for node, out_degree in self.LG.out_degree() if out_degree == 0
            )
        else:
            plan_bis = plan[:-1]
            parent = plan_bis[-1] # self.accepted[(parent, plan_bis)] has been calculated before
            reached = self.get_reached(state, self.accepted[(parent, plan_bis)])
            self.accepted[(state, plan)] = self.accepted[(parent, plan_bis)].union(
                reached
            )

        not_accepted = self.LG.nodes - self.accepted[(state, plan)]
        req_goal = {
            landmark
            for landmark in self.accepted[(state, plan)]
            if not state.issubset(landmark) and self.goals.issubset(landmark)
        }
        req_precon = {
            landmark
            for landmark in self.accepted[(state, plan)]
            if not state.issubset(landmark)
            and len(
                {
                    neighbour
                    for neighbour in self.LG.neighbors(landmark)
                    if not neighbour not in self.accepted[(state, plan)]
                }
            )
        }

        return len(req_goal.union(req_precon, not_accepted))
