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
