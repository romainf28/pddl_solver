
from translate import instantiate
import translate.pddl as pddl
from collections import defaultdict
from itertools import combinations
from formula import Formula


class Encoder:
    def __init__(self, task, horizon):
        self.task = task

        self.horizon = horizon

        self.fluents, self.actions, self.goal = self.ground()

        self.formula = Formula()

        # inverse mapping to store associations between indexes and variables
        self.inverse_mapping = [None]

        # boolean variables for fluents
        self.boolean_variables = defaultdict(dict)
        # propositional variables for actions
        self.action_variables = defaultdict(dict)

    def ground(self):
        (relaxed_reachable, fluent_facts,
            instantiated_actions, instantiated_goal,
            instantiated_axioms, reachable_action_parameters) = instantiate.explore(self.task)

        return fluent_facts, instantiated_actions, instantiated_goal

    def create_variables(self):
        '''First step of the translation from FOL to PL
        Associates an identifier to each action or fluent and store the mappings'''

        idx = 1

        for step in range(self.horizon + 1):
            for fluent in self.fluents:

                self.boolean_variables[step][str(fluent)] = idx
                idx += 1

                self.inverse_mapping.append((str(fluent), step))

        for step in range(self.horizon):
            for act in self.actions:

                self.action_variables[step][act.name] = idx
                idx += 1
                # Inverse mapping
                self.inverse_mapping.append((str(act.name), step))

    def encode_initial_state(self):
        """
        Encodes formula for initial state
        """

        initial = []

        for fact in self.task.init:
            # boolean fluent
            if isinstance(fact, (pddl.conditions.Atom, pddl.conditions.NegatedAtom)):
                if fact in self.fluents:

                    idx = self.boolean_variables[0][str(fact)]
                    initial.append(self.formula.create_var(idx))
            else:
                raise Exception(
                    'Initial condition \'{}\' not recognized'.format(fact))

        # Close-world assumption: if the fluent is not asserted
        # in init formula then it must be set to false.

        for var in self.boolean_variables[0].values():
            v = self.formula.create_var(var)
            if v not in initial:
                not_v = self.formula.make_not(v)
                initial.append(not_v)

        # formula which represents the initial state
        initial_state = self.formula.make_and_from_array(initial)

        return initial_state

    def encode_goal(self):
        """
        Encodes formula for the goal
        """

        propositional_goal = []

        goal = self.task.goal

        # Check if goal is just a single atom
        if isinstance(goal, pddl.conditions.Atom):
            # Check goal is in the variables associated to fluents
            if goal in self.fluents:
                propositional_goal.append(self.formula.create_var(
                    self.boolean_variables[self.horizon][str(goal)]))

        # Check if goal is a conjunction
        elif isinstance(goal, pddl.conditions.Conjunction):
            for fact in goal.parts:

                if fact in self.fluents:
                    goal_idx = self.boolean_variables[self.horizon][str(
                        fact)]
                    propositional_goal.append(
                        self.formula.create_var(goal_idx))

        else:
            raise Exception(
                'Goal condition \'{}\' not recognized'.format(goal))

        # Formula encoding the goal
        goal = self.formula.make_and_from_array(propositional_goal)

        return goal

    def encode_actions(self):
        """
        Encodes action constraints
        """

        actions = []
        action_implication = []

        for step in range(self.horizon):

            for action in self.actions:

                action_name = self.formula.create_var(
                    self.action_variables[step][action.name])

                # Encode preconditions
                preconditions = []
                for precond in action.condition:
                    if precond in self.fluents:
                        preconditions.append(self.formula.create_var(
                            self.boolean_variables[step][str(precond)]))

                # conjunction of all preconditions
                all_preconditions = self.formula.make_and_from_array(
                    preconditions)
                # Action implies the conjunction of all preconditions
                imply_prec = self.formula.make_implication(
                    action_name, all_preconditions)

                # Encode add effects
                add_effects = []
                for add in action.add_effects:
                    add = add[1]
                    if add in self.fluents:
                        add_effects.append(self.formula.create_var(
                            self.boolean_variables[step+1][str(add)]))

                # conjunction of all add effects
                all_add_effects = self.formula.make_and_from_array(add_effects)
                # Action implies the conjunction of all add effects
                imply_add_effects = self.formula.make_implication(
                    action_name, all_add_effects)

                # Encode delete effects
                del_effects = []
                for de in action.del_effects:
                    de = de[1]
                    if de in self.fluents:
                        del_effects.append(self.formula.make_not(
                            self.formula.create_var(self.boolean_variables[step+1][str(de)])))

                # conjunction of all deleted effects
                all_del_effects = self.formula.make_and_from_array(del_effects)
                # Action implies the conjunction of all deleted effects
                imply_del_effects = self.formula.make_implication(
                    action_name, all_del_effects)

                # conjunction of all implications
                action_implication.append(self.formula.make_and_from_array(
                    [imply_prec, imply_add_effects, imply_del_effects]))

            actions.append(
                self.formula.make_and_from_array(action_implication))

        return self.formula.make_and_from_array(actions)

    def encode_frame_axioms(self):
        """
        Encode frame axioms
        """

        all_fluents = []

        actions_deleting = defaultdict(list)
        actions_adding = defaultdict(list)

        # Check if fluent is dynamic
        for fluent in self.fluents:

            for action in self.actions:

                # Check if fluent is added by an action
                for add in action.add_effects:
                    if fluent == add[1]:

                        # Save action and change the value of the fluent from negative to positive
                        actions_adding[fluent].append(action.name)
                        break

                # Check if fluent is a precondition
                if fluent in action.condition:

                    # Check if fluent is deleted by the action
                    for de in action.del_effects:
                        if fluent == de[1]:

                            # Save action and change value of the fluent from positive to negative
                            actions_deleting[fluent].append(action.name)
                            break

        for step in range(self.horizon):
            frame = []

            for fluent in self.fluents:

                pos_actions_done = list()
                neg_actions_done = list()

                swap_pos_to_neg = False
                swap_neg_to_pos = False

                if fluent in actions_adding:
                    swap_neg_to_pos = True
                if fluent in actions_deleting:
                    swap_pos_to_neg = True

                # Same fluent at two consecutive steps
                f_step = self.formula.create_var(
                    self.boolean_variables[step][str(fluent)])
                f_step_plus1 = self.formula.create_var(
                    self.boolean_variables[step + 1][str(fluent)])

                if not (swap_neg_to_pos):
                    # If fluent is false at step i and is also false at step i+1

                    not_f_step = self.formula.make_not(f_step)
                    not_f_step_plus1 = self.formula.make_not(f_step_plus1)

                    frame.append(self.formula.make_implication(
                        not_f_step, not_f_step_plus1))

                else:
                    # The fluent can be added by at least one action

                    not_f_step = self.formula.make_not(f_step)

                    consecutive_fluents = self.formula.make_and(
                        not_f_step, f_step_plus1)

                    # disjunction of all actions that change the fluent's value
                    for act in actions_adding[fluent]:
                        pos_actions_done.append(
                            self.formula.create_var(self.action_variables[step][act]))

                    if len(pos_actions_done) > 1:
                        at_least_one_action = self.formula.make_or_from_array(
                            pos_actions_done)
                    else:
                        at_least_one_action = pos_actions_done[0]

                    frame.append(self.formula.make_implication(
                        consecutive_fluents, at_least_one_action))

                if not (swap_pos_to_neg):
                    # If fluent is true at step i and is also true at step i+1
                    frame.append(self.formula.make_implication(
                        f_step, f_step_plus1))

                else:
                    # The fluent can be deleted by at least one action

                    not_f_stepplus1 = self.formula.make_not(f_step_plus1)

                    consecutive_fluents = self.formula.make_and(
                        f_step, not_f_stepplus1)

                    # disjunction of all actions that change the fluent's value
                    for act in actions_deleting[fluent]:
                        neg_actions_done.append(
                            self.formula.create_var(self.action_variables[step][act]))

                    if len(neg_actions_done) > 1:
                        at_least_one_action = self.formula.make_or_from_array(
                            neg_actions_done)
                    else:
                        at_least_one_action = neg_actions_done[0]

                    frame.append(self.formula.make_implication(
                        consecutive_fluents, at_least_one_action))

            all_fluents.append(self.formula.make_and_from_array(frame))

        return self.formula.make_and_from_array(all_fluents)

    def encode_at_most_one_action(self):
        '''
        Encodes at most one action axiom
        '''
        one_action = []

        for step in range(self.horizon):

            negated_couple = []

            v = self.action_variables[step]
            for action1, action2 in combinations(v.values(), 2):

                action_couple = self.formula.create_var_array(
                    [action1, action2])
                conjunction_couple = self.formula.make_and_from_array(
                    action_couple)
                negated_couple.append(
                    self.formula.make_not(conjunction_couple))

            one_action.append(self.formula.make_and_from_array(negated_couple))

        return self.formula.make_and_from_array(one_action)

    def encode_at_least_one_action(self):
        '''
        Encodes at least one action per step axiom
        '''

        at_least_one_for_step = []
        at_least_one = []

        for step in range(self.horizon):

            for action in self.actions:
                action_idx = self.action_variables[step][str(action.name)]
                at_least_one_for_step.append(
                    self.formula.create_var(action_idx))

            # at least one action should be performed at each step
            at_least_one.append(
                self.formula.make_or_from_array(at_least_one_for_step))

        return self.formula.make_and_from_array(at_least_one)
