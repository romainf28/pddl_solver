
from grounder import Grounder
import pddlparser
from GraphPlanRelaxed import GraphPlanRelaxed


domain_file = 'instances/groupe2/domain.pddl'
problem_file = 'instances/groupe2/problem0.pddl'

domain = pddlparser.PDDLParser.parse(domain_file)
problem = pddlparser.PDDLParser.parse(problem_file)

grounder = Grounder(domain, problem)
task = grounder.ground()



graph_plan = GraphPlanRelaxed(task)
print(graph_plan.get_FF_heuristic())
