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
