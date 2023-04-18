from pddlparser import PDDLParser
from grounder import Grounder
from plan_extractor import PlanExtractor
from minisat_utils import MinisatSolver


class SATPlanner:

    def __init__(self, domain_file, problem_file, custom_assigner=None):
        self.domain = PDDLParser.parse(domain_file)
        self.problem = PDDLParser.parse(problem_file)
        self.custom_assigner = custom_assigner

        grounder = Grounder(self.domain, self.problem,
                            custom_assigner=custom_assigner)
        self.task = grounder.ground()

    def find_plan(self, min_horizon=1, max_horizon=10):
        '''
        Try to find a plan for differents horizons varying between min_horizon and max_horizon
        '''
        solver = MinisatSolver()
        plan_extractor = PlanExtractor(self.task)
        print('looking for a plan with {} actions ...'.format(min_horizon))
        formula = plan_extractor.encode_plan_formula(min_horizon)

        valuation = solver.solve(formula)
        plan = plan_extractor.extract_plan(self.task.operators, valuation)

        if plan:
            print('Plan with {} actions found'.format(min_horizon))
            return plan
        else:
            while plan_extractor.last_horizon <= max_horizon:
                print('looking for a plan with {} actions ...'.format(
                    plan_extractor.last_horizon+1))
                formula = plan_extractor.encode_formula_next_horizon()
                valuation = solver.solve(formula)
                plan = plan_extractor.extract_plan(
                    self.task.operators, valuation)
                if plan:
                    print('Plan with {} actions found'.format(
                        plan_extractor.last_horizon))
                    return plan
        print('No plan with less than {} actions found'.format(max_horizon))
        return plan
