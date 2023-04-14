from planning_task import PlanningTask
from collections import defaultdict


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

    def extract_plan(self, operators, valuation):
        '''
        Transforms a valuation i.e. a list of facts into a list of operators
        '''
        positive_facts = defaultdict(set)
        negative_facts = defaultdict(set)
        plan_length = -1

        for fact in valuation:
            if ('<->' in fact) or ('AND' in fact):
                continue

            parts = fact.split('-')
            depth = int(parts[-1])
            plan_length = max(plan_length, depth)

            if fact.startswith("not-"):
                variable_name = "-".join(parts[:-1])
                negative_facts[depth].add(variable_name)
            else:
                variable_name = "-".join(parts[:-1])
                positive_facts[depth].add(variable_name)

        plan = []
        for step in range(plan_length):
            current_state = positive_facts[step]
            next_state = positive_facts[step+1]
            print(current_state, next_state)
            chosen_operator = None
            for op in operators:
                if op.applicable(current_state):
                    print(op.apply(current_state), next_state)
                if op.applicable(current_state) and op.apply(current_state) == next_state:
                    chosen_operator = op
                    break
            plan.append(chosen_operator)
        return plan
