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

from PDDL import PDDL_Parser
import time
from utils import (get_static_and_dynamic_predicates, get_timeless_truth,
                   check_negative_preconditions, check_positive_preconditions,
                   check_action_parameters, predicate_to_string, action_to_string)
from pysat.solvers import Glucose3


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
        self.positive_goals = parser.positive_goals
        self.negative_goals = parser.negative_goals
        self.step = 0
        self.idx = 0

        # index which maps the propositional variables to integers to store clauses in a more convenient way
        self.variable_index = {}

        # dictionnary in which the keys are the index of some predicates and the values are the index of the positive preconditions
        self.dict_positive_preconditions = {}
        self.dict_negative_preconditions = {}

    def filter_valid_actions(self, fixed_predicates, timeless_truth):
        '''
        Groundify the domain actions and eliminates those which will never be applicable because of the truth value of predicates in their preconditions.
        Also eliminates groundified actions with duplicates parameters.
        '''
        filtered_actions = []

        for action in self.actions:
            for groundified_action in action.groundify(self.objects, self.types):

                valid = check_positive_preconditions(groundified_action, fixed_predicates, timeless_truth) and check_negative_preconditions(
                    groundified_action, fixed_predicates, timeless_truth) and check_action_parameters(groundified_action)
                if valid:
                    filtered_actions.append(groundified_action)

        return filtered_actions

    def get_fulfilled_positive_preconditions(self, action, dynamic_predicates, old_predicates):
        '''
        Returns the list of positive preconditions of an action which are satisfied in the current state and a boolean 
        to indicate whether all positive preconditions are satisfied or not.
        '''
        fulfilled_pos_precond = []
        all_positive_precond_fulfilled = True
        for positive_precondition in action.positive_preconditions:
            if positive_precondition[0] in dynamic_predicates:
                valid_precond = False
                for pred in old_predicates:
                    if pred == predicate_to_string(positive_precondition):
                        fulfilled_pos_precond.append(pred)
                        valid_precond = True
                        break
                if not (valid_precond):
                    all_positive_precond_fulfilled = False
        return fulfilled_pos_precond, all_positive_precond_fulfilled

    def get_fulfilled_negative_preconditions(self, action, dynamic_predicates, old_predicates):
        '''
        Returns the list of negative preconditions of an action which are satisfied in the current state
        '''
        fulfilled_neg_precond = []
        for negative_precondition in action.negative_preconditions:
            if negative_precondition[0] in dynamic_predicates:
                for pred in old_predicates:
                    if pred == predicate_to_string(negative_precondition):
                        fulfilled_neg_precond.append(pred)
                        break
        return fulfilled_neg_precond

    def update_clauses_with_action_preconditions(self, satisfied_positive_preconditions, satisfied_negative_preconditions, new_clauses, idx1):
        '''
        Updates the clauses with the satisfied positive and negative preconditions of an action
        '''
        for pred in satisfied_positive_preconditions:
            new_clauses.append(
                [-idx1, self.variable_index[pred+'.'+str(self.step-1)]])
        for pred in satisfied_negative_preconditions:
            new_clauses.append(
                [-idx1, -self.variable_index[pred+'.'+str(self.step-1)]])

    def update_clauses_with_positive_action_effects(self, action, new_predicates, new_clauses, new_propositional_variables, idx1):
        '''
        Updates the clauses with the effects of an action
        '''
        for pos_effect in action.add_effects:
            positive_predicate = predicate_to_string(pos_effect)
            if positive_predicate not in new_predicates:
                new_predicates.append(positive_predicate)
                new_propositional_variables.append(
                    positive_predicate + '.' + str(self.step))
                self.variable_index[positive_predicate +
                                    '.' + str(self.step)] = self.idx
                self.dict_positive_preconditions[self.idx] = []
                self.dict_negative_preconditions[self.idx] = []
                self.idx += 1
            idx2 = self.variable_index[positive_predicate +
                                       '.' + str(self.step)]
            self.dict_positive_preconditions[idx2].append(
                idx1)
            new_clauses.append([-idx1, idx2])

    def update_clauses(self, satisfied_positive_preconditions, satisfied_negative_preconditions, action, new_actions, new_clauses, new_predicates, new_propositional_variables):
        '''
        Updates clauses at a given step with the preconditions and positive effects of applicable groundified actions
        '''
        new_actions.append(action)
        new_variable_name = action_to_string(
            action) + '.' + str(self.step)
        new_propositional_variables.append(new_variable_name)
        self.variable_index[new_variable_name] = self.idx
        idx1 = self.idx
        self.idx += 1

        self.update_clauses_with_action_preconditions(
            satisfied_positive_preconditions, satisfied_negative_preconditions, new_clauses, idx1)

        self.update_clauses_with_positive_action_effects(
            action, new_predicates, new_clauses, new_propositional_variables, idx1)

    def update_predicates(self, old_predicates, new_predicates, new_propositional_variables):
        '''
        Updates propositional variables with new predicates
        '''
        for old_predicate in old_predicates:
            if old_predicate not in new_predicates:
                new_predicates.append(old_predicate)
                new_propositional_variables.append(
                    old_predicate+'.'+str(self.step))
                self.variable_index[old_predicate +
                                    '.'+str(self.step)] = self.idx
                self.dict_positive_preconditions[self.idx] = []
                self.dict_negative_preconditions[self.idx] = []
                self.idx += 1

    def update_clauses_with_negative_actions_effects(self, new_actions, new_predicates, new_clauses):
        for action in new_actions:
            idx1 = self.variable_index[action_to_string(
                action)+'.'+str(self.step)]
            for negative_effect in action.del_effects:
                pred = predicate_to_string(negative_effect)
                if pred in new_predicates:
                    idx2 = self.variable_index[pred+'.'+str(self.step)]
                    self.dict_negative_preconditions[self.variable_index[pred+'.'+str(
                        self.step)]].append(idx1)
                    new_clauses.append([-idx1, -idx2])

    def update_clauses_with_new_actions(self, new_actions, new_clauses):
        for i in range(len(new_actions)):
            for j in range(i+1, len(new_actions)):
                ii = self.variable_index[action_to_string(
                    new_actions[i])+'.'+str(self.step)]
                jj = self.variable_index[action_to_string(
                    new_actions[j])+'.'+str(self.step)]
                new_clauses.append([-ii, -jj])

    def update_clauses_with_new_predicates(self, old_predicates, new_predicates, new_clauses):
        for pred in new_predicates:
            is_new_pred = False
            i = self.variable_index[pred+'.'+str(self.step)]
            clause_pos = [-i]
            clause_neg = [i]
            if pred in old_predicates:
                j = self.variable_index[pred+'.'+str(self.step-1)]
                clause_pos.append(j)
                clause_neg.append(-j)
            else:
                is_new_pred = True
            for k in self.dict_positive_preconditions[i]:
                clause_pos.append(k)
            for k in self.dict_negative_preconditions[i]:
                clause_neg.append(k)
            new_clauses.append(clause_pos)
            if not is_new_pred:

                new_clauses.append(clause_neg)

    def generate_goal_clause(self, pos_goals, neg_goals):
        goal_clause = []
        for k in pos_goals:
            goal_clause.append([k])
        for k in neg_goals:
            goal_clause.append([-k])
        return goal_clause

    def solve(self):
        # Initialise clock
        t0 = time.time()

        static_predicates, dynamic_predicates = get_static_and_dynamic_predicates(
            self.predicates, self.actions)

        timeless_truth = get_timeless_truth(self.state, static_predicates)
        valid_groundified_actions = self.filter_valid_actions(
            static_predicates, timeless_truth)

        old_predicates = []
        for pred in self.state:
            if pred[0] in dynamic_predicates:
                old_predicates.append(predicate_to_string(pred))

        propositional_variables = [None]
        old_clauses = []
        self.idx = 1

        for pred in old_predicates:
            self.variable_index[pred+'.0'] = self.idx
            propositional_variables.append(pred+'.0')
            old_clauses.append([self.idx])
            self.idx += 1

        while True:
            new_clauses = []
            self.step += 1

            print('Step {}'.format(self.step))
            print('======================')

            new_propositional_variables = []
            new_predicates = []
            new_actions = []

            for action in valid_groundified_actions:
                satisfied_pos_precond, all_pos_precond_satisfied = self.get_fulfilled_positive_preconditions(
                    action, dynamic_predicates, old_predicates)
                if all_pos_precond_satisfied:
                    satisfied_neg_precond = self.get_fulfilled_negative_preconditions(
                        action, dynamic_predicates, old_predicates)

                    self.update_clauses(satisfied_pos_precond, satisfied_neg_precond,
                                        action, new_actions, new_clauses, new_predicates, new_propositional_variables)

            self.update_predicates(
                old_predicates, new_predicates, new_propositional_variables)

            self.update_clauses_with_negative_actions_effects(
                new_actions, new_predicates, new_clauses)

            self.update_clauses_with_new_actions(new_actions, new_clauses)

            self.update_clauses_with_new_predicates(
                old_predicates, new_predicates, new_clauses)

            old_predicates = new_predicates
            propositional_variables += new_propositional_variables
            old_clauses += new_clauses

            feasible = True
            pos_goals = []
            neg_goals = []
            for goal_pos in self.positive_goals:
                if predicate_to_string(goal_pos) not in new_predicates:
                    feasible = False
                    break
                else:
                    pos_goals.append(
                        self.variable_index[predicate_to_string(goal_pos)+'.'+str(self.step)])
            for goal_neg in self.negative_goals:
                if predicate_to_string(goal_neg) in new_predicates:
                    neg_goals.append(
                        self.variable_index[predicate_to_string(goal_neg)+'.'+str(self.step)])

            if not feasible:
                print("No conceivable solution yet ...")

            else:
                goal_clause = self.generate_goal_clause(pos_goals, neg_goals)

                sat_clauses = old_clauses + goal_clause

                g = Glucose3()
                for clause in sat_clauses:
                    g.add_clause(clause)

                if g.solve():
                    print('Solution found !')
                    plan = []
                    model = g.get_model()
                    for t in range(self.step+1):
                        for action in valid_groundified_actions:
                            if action_to_string(action)+'.'+str(t) in propositional_variables:
                                idx = self.variable_index[action_to_string(
                                    action)+'.'+str(t)]
                                if int(model[idx-1]) > 0:
                                    plan.append(action)
                    print("Plan found : ")
                    for action in plan:
                        print(action)
                    print("Number of steps : "+str(self.step))
                    return plan

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
    planner = SATPlanner(domain, problem)
    plan = planner.solve()
    # print('Time: ' + str(time.time() - start_time) + 's')
    # if plan is not None:
    #     print('plan:')
    #     for act in plan:
    #         print(act if verbose else act.name +
    #               ' ' + ' '.join(act.parameters))
    # else:
    #     sys.exit('No plan was found')
