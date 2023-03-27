#!/usr/bin/env python
# Four spaces as indentation [no tabs]

# This file is part of PDDL Parser, available at <https://github.com/pucrs-automated-planning/pddl-parser>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from .PDDL import PDDL_Parser
import time
from utils import (get_static_and_dynamic_preidcates, get_timeless_truth,
                   check_negative_preconditions, check_positive_preconditions,
                   check_action_parameters, predicate_to_string, action_to_string)


class SATPlanner:

    def __init__(self, domain_path, problem_path):
        parser = PDDL_Parser()
        parser.parse_domain(domain_path)
        parser.parse_problem(problem_path)
        self.state = parser.state
        self.predicates = parser.predicates
        self.actions = parser.actions
        self.objects = parser.objects
        self.types = parser.types
        self.step = 0
        self.idx = 0
        self.reverse_index = {}
        self.dict_positive_preconditions = {}
        self.dict_negative_preconditions = {}

    def filter_valid_actions(self, fixed_predicates, timeless_truth):
        filtered_actions = []

        for action in self.actions:
            for groundified_action in action.groundify(self.objects, self.types):

                valid = check_positive_preconditions(groundified_action, fixed_predicates, timeless_truth) and check_negative_preconditions(
                    groundified_action, fixed_predicates, timeless_truth) and check_action_parameters(groundified_action)
                if valid:
                    filtered_actions.append(groundified_action)

        return filtered_actions

    def get_fulfilled_positive_preconditions(self, action, dynamic_predicates, old_dynamic_predicates):
        fulfilled_pos_precond = []
        all_positive_precond_fulfilled = True
        for positive_precondition in action.positive_preconditions:
            if positive_precondition[0] in dynamic_predicates:
                valid_precond = False
                for pred in old_dynamic_predicates:
                    if pred == predicate_to_string(positive_precondition):
                        fulfilled_pos_precond.append(pred)
                        valid_precond = True
                        break
                if not (valid_precond):
                    all_positive_precond_fulfilled = False
        return fulfilled_pos_precond, all_positive_precond_fulfilled

    def get_fulfilled_negative_preconditions(self, action, dynamic_predicates, old_dynamic_predicates):
        fulfilled_neg_precond = []
        for negative_precondition in action.negative_preconditions:
            if negative_precondition[0] in dynamic_predicates:
                for pred in old_dynamic_predicates:
                    if pred == predicate_to_string(negative_precondition):
                        fulfilled_neg_precond.append(pred)
                        break
        return fulfilled_neg_precond

    def update_clauses(self, satisfied_positive_preconditions, satisfied_negative_preconditions, action, new_actions, new_clause, new_predicates, new_variables):
        new_actions.append(action)
        new_variable_name = action_to_string(
            action) + '.' + str(self.step)
        new_variables.append(new_variable_name)
        self.reverse_index[new_variable_name] = self.idx
        idx1 = self.idx
        self.idx += 1

        for pred in satisfied_positive_preconditions:
            new_clause.append(
                [-idx1, self.reverse_index[pred+'.'+str(self.step-1)]])
        for pred in satisfied_negative_preconditions:
            new_clause.append(
                [-idx1, -self.reverse_index[pred+'.'+str(self.step-1)]])
        for pos_effect in action.add_effects:
            positive_predicate = predicate_to_string(pos_effect)
            if positive_predicate not in new_predicates:
                new_predicates.append(positive_predicate)
                new_variables.append(
                    positive_predicate + '.' + str(self.step))
                self.reverse_index[positive_predicate +
                                   '.' + str(self.step)] = self.idx
                self.dict_positive_preconditions[self.idx] = []
                self.dict_negative_preconditions[self.idx] = []
                self.idx += 1
            idx2 = self.reverse_index[positive_predicate +
                                      '.' + str(self.step)]
            self.dict_positive_preconditions[idx2].append(
                idx1)
            new_clause.append([-idx1, idx2])

    def update_predicates(self, old_predicates, new_predicates, new_variables):
        for old_predicate in old_predicates:
            if old_predicate not in new_predicates:
                new_predicates.append(old_predicate)
                new_variables.append(old_predicate+'.'+str(self.step))
                self.reverse_index[old_predicate+'.'+str(self.step)] = self.idx
                self.dict_positive_preconditions[self.idx] = []
                self.dict_negative_preconditions[self.idx] = []
                self.idx += 1

    def solve(self, domain, problem):
        # Initialise clock
        t0 = time.time()

        static_predicates, dynamic_predicates = get_static_and_dynamic_preidcates(
            self.predicates, self.actions)

        timeless_truth = get_timeless_truth(self.state, static_predicates)
        valid_groundified_actions = self.filter_valid_actions(
            static_predicates, timeless_truth)

        old_dynamic_predicates = []
        for pred in self.state:
            if pred[0] in dynamic_predicates:
                old_dynamic_predicates.appennd(predicate_to_string(pred))

        variables = [None]
        old_clause = []
        self.idx = 1

        for pred in old_dynamic_predicates:
            self.reverse_index[pred+'.0'] = self.idx
            variables.append(pred+'.0')
            old_clause.append([self.idx])
            self.idx += 1

        while True:
            new_clause = []
            self.step += 1

            print('Step {}'.format(self.step))
            print('======================')

            new_variables = []
            new_predicates = []
            new_actions = []

            for action in valid_groundified_actions:
                satisfied_pos_precond, all_pos_precond_satisfied = self.get_fulfilled_positive_preconditions(
                    action, dynamic_predicates, old_dynamic_predicates)
                if all_pos_precond_satisfied:
                    satisfied_neg_precond = self.get_fulfilled_negative_preconditions(
                        action, dynamic_predicates, old_dynamic_predicates)

                    self.update_clauses(satisfied_pos_precond, satisfied_neg_precond,
                                        action, new_actions, new_clause, new_predicates, new_variables)

            self.update_predicates(
                old_dynamic_predicates, new_predicates, new_variables)

        # # Parsed data
        # state = parser.state
        # goal_pos = parser.positive_goals
        # goal_not = parser.negative_goals
        # # Do nothing
        # if self.applicable(state, goal_pos, goal_not):

        #     return []
        # # Grounding process
        # ground_actions = []
        # for action in parser.actions:
        #     for act in action.groundify(parser.objects, parser.types):
        #         ground_actions.append(act)
        # # Search
        # visited = set([state])
        # fringe = [state, None]
        # while fringe:
        #     state = fringe.pop(0)
        #     plan = fringe.pop(0)
        #     for act in ground_actions:
        #         if self.applicable(state, act.positive_preconditions, act.negative_preconditions):
        #             new_state = self.apply(
        #                 state, act.add_effects, act.del_effects)
        #             if new_state not in visited:
        #                 if self.applicable(new_state, goal_pos, goal_not):
        #                     full_plan = [act]
        #                     while plan:
        #                         act, plan = plan
        #                         full_plan.insert(0, act)
        #                     return full_plan
        #                 visited.add(new_state)
        #                 fringe.append(new_state)
        #                 fringe.append((act, plan))
        # return None

    # -----------------------------------------------
    # Applicable
    # -----------------------------------------------

    def applicable(self, state, positive, negative):
        return positive.issubset(state) and negative.isdisjoint(state)

    # -----------------------------------------------
    # Apply
    # -----------------------------------------------

    def apply(self, state, positive, negative):
        return state.difference(negative).union(positive)


# -----------------------------------------------
# Main
# -----------------------------------------------
if __name__ == '__main__':
    import sys
    import time
    start_time = time.time()
    domain = sys.argv[1]
    problem = sys.argv[2]
    verbose = len(sys.argv) > 3 and sys.argv[3] == '-v'
    planner = Planner()
    plan = planner.solve(domain, problem)
    print('Time: ' + str(time.time() - start_time) + 's')
    if plan is not None:
        print('plan:')
        for act in plan:
            print(act if verbose else act.name +
                  ' ' + ' '.join(act.parameters))
    else:
        sys.exit('No plan was found')
