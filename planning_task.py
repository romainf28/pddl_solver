class Operator:
    """
    The preconditions are the facts that must be true
    to apply the operator.
    add_effects are the facts made true by the operator.
    delete_effects are the facts made false by the operator.
    """

    def __init__(self, name, preconditions, add_effects, del_effects):
        self.name = name
        self.preconditions = frozenset(preconditions)
        self.add_effects = frozenset(add_effects)
        self.del_effects = frozenset(del_effects)

    def applicable(self, state):
        """
        Operators are applicable when their preconditions form a subset
        of the facts in a given state.
        """
        return self.preconditions.issubset(state)

    def apply(self, state):
        """
        Apply the operator in a given state
        """
        assert self.applicable(state)
        return state.difference(self.del_effects).union(self.add_effects)

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.preconditions == other.preconditions
            and self.add_effects == other.add_effects
            and self.del_effects == other.del_effects
        )

    def __hash__(self):
        return hash((self.name, self.preconditions, self.add_effects, self.del_effects))

    def __str__(self):
        str_repr = "%s\n" % self.name
        for gp, facts in [
            ("PRE", self.preconditions),
            ("ADD", self.add_effects),
            ("DEL", self.del_effects),
        ]:
            for fact in facts:
                str_repr += f"  {gp}: {fact}\n"
        return str_repr

    def __repr__(self):
        return "<Operator %s>" % self.name


class PlanningTask:
    """
    A PDDL planning task
    """

    def __init__(self, name, facts, initial_state, goals, operators):
        """
        Parameters :
        - name : the name of the task
        - facts :  all the facts that are valid in the domain
        - initial_state : facts that are true at the beginning
        - goals : facts that must be true to solve the problem
        - operators : set of operator instances 
        """
        self.name = name
        self.facts = facts
        self.initial_state = initial_state
        self.goals = goals
        self.operators = operators

    def is_goal_reached(self, state):
        return self.goals.issubset(state)

    def get_next_states(self, state):
        """
        Returns a list of (op, new_state) pairs where "op" is an applicable
        operator and "new_state" is the state obtained after applying op in new_state
        """
        return [(op, op.apply(state)) for op in self.operators if op.applicable(state)]

    def __str__(self):
        str_repr = "Task {0}\n  Facts:  {1}\n  Initial state:  {2}\n  Goals: {3}\n  Operators:   {4}"
        return str_repr.format(
            self.name,
            ", ".join(self.facts),
            self.initial_state,
            self.goals,
            "\n".join(map(repr, self.operators)),
        )

    def __repr__(self):
        string = "<Task {0}, num_facts: {1}, num_operators: {2}>"
        return string.format(self.name, len(self.facts), len(self.operators))
