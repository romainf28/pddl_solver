
from translate import instantiate
import translate.pddl as pddl
from collections import defaultdict
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
