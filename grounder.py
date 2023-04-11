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
