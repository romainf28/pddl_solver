from planning_task import PlanningTask


class PlanExtractor:

    def __init__(self, task: PlanningTask, horizon: int):
        self.task = task
        self.horizon = horizon

    def encode_plan_formula(self):
        """
        Encodes a given PDDL task with a given horizon into a logical formula
        """
        init_facts_true = list(sorted(self.task.initial_state))
        init_facts_false = list(
            sorted(self.task.facts - self.task.initial_state))

        positive_fluents = [self._get_fluent_string(
            fact, 0) for fact in init_facts_true]
        negative_fluents = [self._get_fluent_string(
            fact, 0, negated=True) for fact in init_facts_false]

        formula = positive_fluents + negative_fluents

        for step in range(self.horizon):
            disjunction = []
            for op in self.task.operators:
                disjunction.append(self._get_formula_for_operator(
                    op, step))
            formula.append(disjunction)

        goal = [self._get_fluent_string(fact, self.horizon)
                for fact in list(sorted(self.task.goals))]
        formula.extend(goal)

        return formula

    def _get_fluent_string(self, fact, step, negated=False):
        """
        Returns a string representing a fluent. The representation contains the fluent name 
        preceded by a 'not' if it is negated and the step number
        """
        name = str(fact)
        if negated:
            name = "not-" + name
        return "{}-{}".format(name, step)

    def _get_formula_for_fact(self, operator, fact, step):
        """
        Returns a formula to encode the fluent representing 'fact' at step 'step'
        """
        # if the operator makes fact true at step +1 (the fact is in the add effects of the operator)
        if fact in operator.add_effects:
            return [self._get_fluent_string(fact, step+1)]
        # if the fact does not occur in the operator effects : the fluents reprsenting the facts at step and step+1 are equivalent
        if not fact in operator.del_effects:
            return ['<->'.join([self._get_fluent_string(fact, step+1), self._get_fluent_string(fact, step)])]
        # if the operator makes fact false at step+1 (the fact is in the del effects of the operator)
        else:
            return [self._get_fluent_string(fact, step+1, negated=True)]

    def _get_formula_for_operator(self, operator, step):
        """
        Retruns a formula representing an operator at a given step
        """
        preconditions = list(sorted(operator.preconditions))
        formula = [self._get_fluent_string(fact, step)
                   for fact in preconditions]
        for fact in self.task.facts:
            formula += self._get_formula_for_fact(operator, fact, step)
        return formula
