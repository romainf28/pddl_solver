
from grounder import Grounder
import pddlparser
from plan_extractor import PlanExtractor

domain_file = 'instances/groupe1/domain.pddl'
problem_file = 'instances/groupe1/problem0.pddl'

domain = pddlparser.PDDLParser.parse(domain_file)
problem = pddlparser.PDDLParser.parse(problem_file)


grounder = Grounder(domain, problem)
task = grounder.ground()

plan_extractor = PlanExtractor(task, 10)
print(plan_extractor.encode_plan_formula())
