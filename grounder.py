from collections import defaultdict
import itertools
import re

from planning_task import Operator, PlanningTask


class Grounder:
    """
    A class to ground a PDDL domain and problem into a Planning Task
    """

    def __init__(self, domain, problem):
        self.domain = domain
        self.problem = problem
        self.actions = domain.actions
        self.predicates = domain.predicates

        # Dictionnary type -> objects
        self.type2objects = problem.initial_state.objects
        self.type2objects.update(domain.constants)

    def ground(self):
        # Get the static predicates
        static_predicates = self._get_static_predicates()

        # Get string representation of the atoms in the initial state
        initial_state = self._get_partial_state(
            self.problem.initial_state.predicates)

        # Ground actions
        operators = self._ground_actions(
            static_predicates, initial_state)

        # Ground goal
        goals = self._get_partial_state(self.problem.goals)

        # get facts from operators and include the ones from the goal
        facts = self._get_facts_from_operators(operators) | goals

        # Remove static predicates from initial state
        initial_state &= facts

        # remove irrelevant operators
        operators = self._remove_irrelevant_operators(operators, goals)

        return PlanningTask(self.domain.name, facts, initial_state, goals, operators)

    def _get_static_predicates(self):
        """
        Returns the list of static predicates, i.e. predicates which
        don't occur in an effect of an action.
        """

        def get_effects(action):
            effects = set()
            for effect in action.effects.literals:
                # handle del effects
                if effect[0] == -1:
                    effect = effect[1]
                effects.add(effect[0])
            return effects

        effects = [get_effects(action) for action in self.actions]
        effects = set(itertools.chain(*effects))

        def is_static(predicate):
            return not any(predicate[0] == eff for eff in effects)

        static_predicates = [pred[0]
                             for pred in self.predicates if is_static(pred)]
        return static_predicates

    def _get_grounded_string(self, name, args):
        """Return a more convenient string representation for a predicate"""
        args_string = " " + " ".join(args) if args else ""
        return "({}{})".format(name, args_string)

    def _get_fact(self, atom):
        """Return the string representation of a grounded atom."""
        return self._get_grounded_string(atom[0], atom[1:])

    def _get_partial_state(self, atoms):
        """Return a set of the string representation of the grounded atoms."""
        return frozenset(self._get_fact(atom) for atom in atoms)

    def _find_pred_in_initial_state(self, pred_name, param, pos, initial_state):
        """
        Check if there is an instantiation of the predicate pred_name
        with the parameter param at position pos in the initial condition
        """
        match_in_initial_state = None
        if pos == 0:
            match_in_initial_state = re.compile(rf"\({pred_name} {param}.*")
        else:
            reg_ex = r"\(%s\s+" % pred_name
            reg_ex += r"[\w\d-]+\s+" * pos
            reg_ex += "{}.*".format(param)
            match_in_initial_state = re.compile(reg_ex)
        assert match_in_initial_state is not None
        return any([match_in_initial_state.match(string) for string in initial_state])

    def _get_action_signature(self, action):
        """
        Get the signature of an action, i.e. a list of pairs (param, param_type) 
        for each parameter of the action
        """
        return list(zip(action.arg_names, action.types))

    def _ground_atom(self, atom, assignment, action_signature):
        """
        Return the grounded representation of an atom with respect
        to an assignment.
        """
        names = []
        for name, _ in action_signature:

            if name in assignment and name in atom:
                names.append(assignment[name])

        return self._get_grounded_string(atom[0], names)

    def _create_operator(self, action, assignment, static_predicates, initial_state):
        """Create a new operator for an action with a given assignment.
        True static predicates are not added to the
        precondition facts. If there is a false static predicate
        in the ungrounded precondition, the operator won't be created.
        """
        precondition_facts = set()
        action_signature = self._get_action_signature(action)
        for precondition in action.preconditions.literals:
            # handle negative preconditions
            if precondition[0] == -1:
                precondition = precondition[1]
            fact = self._ground_atom(precondition, assignment, action_signature
                                     )
            predicate_name = precondition[0]

            if predicate_name in static_predicates:
                # Check if this precondition is false in the initial state
                if fact not in initial_state:
                    # the precondition will never be true, hence we don't add the operator
                    return None
            else:
                # the precondition is not always true -> we add the operator
                precondition_facts.add(fact)

        add_effects = set()
        del_effects = set()

        for effect in action.effects.literals:
            # del effects
            if effect[0] == -1:
                fact = self._ground_atom(
                    effect[1], assignment, action_signature)
                del_effects.add(fact)
            else:
                # add effects
                fact = self._ground_atom(effect, assignment, action_signature)
                add_effects.add(fact)

        # If the same fact is added and deleted by an operator, the STRIPS formalism
        # adds it.
        del_effects -= add_effects
        add_effects -= precondition_facts
        args = [assignment[arg_name] for arg_name in action.arg_names]
        name = self._get_grounded_string(action.name, args)
        return Operator(name, precondition_facts, add_effects, del_effects)

    def _ground_action(self, action, static_predicates, initial_state):
        """
        Ground the action and return a list of operators.
        """
        param2objects = {}

        for idx, param_type in enumerate(action.types):
            # set of possible objects for this parameter
            objects = set(self.type2objects[param_type])
            param2objects[action.arg_names[idx]] = objects

        # For each parameter that is not constant,
        # remove all invalid static precondition
        for param, objects in param2objects.items():
            for pred in action.preconditions.literals:
                # handle negative preconditions
                if pred[0] == -1:
                    pred = pred[1]

                # if a static predicate is present in the precondition
                if pred[0] in static_predicates:
                    pos = -1
                    count = 0
                    # check if there is an instantiation with the current parameter
                    for sig_var, _ in self._get_action_signature(action):
                        if sig_var == param:
                            pos = count
                        count += 1
                    if pos != -1:
                        # remove object if there is no instantiation in the initial state
                        obj_copy = objects.copy()
                        for o in obj_copy:
                            if not self._find_pred_in_initial_state(pred[0], o, pos, initial_state):
                                objects.remove(o)

        # list of possible assignment tuples (param_name, object)
        possible_assignments = [
            [(param, obj) for obj in objects] for param, objects in param2objects.items()
        ]
        # Calculate all possible assignments
        assignments = itertools.product(*possible_assignments)

        # Create a new operator for each possible assignment
        operators = [
            self._create_operator(action, dict(assign), static_predicates, initial_state) for assign in assignments
        ]

        # Filter out None values
        operators = filter(bool, operators)

        return operators

    def _ground_actions(self, static_predicates, initial_state):
        """
        Ground all the actions and return a list of operators.
        """
        op_list = [self._ground_action(action, static_predicates, initial_state)
                   for action in self.actions]
        grounded_operators = list(itertools.chain(*op_list))
        return grounded_operators

    def _get_facts_from_operators(self, operators):
        """
        Get all the facts from grounded operators (precondition, add
        effects and delete effects).
        """
        facts = set()
        for op in operators:
            facts |= op.preconditions | op.add_effects | op.del_effects

        return facts

    def _remove_irrelevant_operators(self, operators, goals):
        """
        From the facts within the goal state we iteratively compute
        a fixpoint of all relevant effects.
        Relevant effects are those which contribute to a valid path to the goal.
        """

        relevant_facts = set()
        old_relevant_facts = set()
        changed = True
        for goal in goals:
            relevant_facts.add(goal)

        while changed:
            # set next relevant facts to current facts
            # if nothing is added in the for loop a
            # fixpoint has been found
            old_relevant_facts = relevant_facts.copy()

            for op in operators:
                new_add_list = op.add_effects & relevant_facts
                new_del_list = op.del_effects & relevant_facts
                if new_add_list or new_del_list:
                    # add all preconditions to the relevant facts
                    relevant_facts |= op.preconditions
            changed = old_relevant_facts != relevant_facts

        # delete all effects which are not relevant
        del_operators = set()
        for op in operators:

            new_add_list = op.add_effects & relevant_facts
            new_del_list = op.del_effects & relevant_facts

            op.add_effects = new_add_list
            op.del_effects = new_del_list
            if not new_add_list and not new_del_list:
                del_operators.add(op)

        # remove completely irrelevant operators
        return [op for op in operators if not op in del_operators]
