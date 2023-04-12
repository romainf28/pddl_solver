
from grounder import Grounder
import pddlparser

domain_file = 'instances/groupe1/domain.pddl'
problem_file = 'instances/groupe1/problem0.pddl'

domain = pddlparser.PDDLParser.parse(domain_file)
problem = pddlparser.PDDLParser.parse(problem_file)


grounder = Grounder(domain, problem)
print(grounder.ground())
