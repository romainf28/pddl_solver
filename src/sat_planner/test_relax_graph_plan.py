
from src.grounder import Grounder
import src.pddlparser as pddlparser
from sat_planner.GraphPlanRelaxed import GraphPlanRelaxed


domain_file = 'instances/groupe3/domain.pddl'
problem_file = 'instances/groupe3/problem1.pddl'

domain = pddlparser.PDDLParser.parse(domain_file)
problem = pddlparser.PDDLParser.parse(problem_file)

grounder = Grounder(domain, problem)
task = grounder.ground()


graph_plan = GraphPlanRelaxed(task)
print(graph_plan.get_FF_heuristic())
