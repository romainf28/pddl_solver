
from src.heuristics.weighted_astar import weighted_astar_search
from src.grounder import Grounder
import src.pddlparser as pddlparser
from src.heuristics.landmarks import LandmarkHeuristic

domain_file = 'src/instances/groupe2/domain.pddl'
problem_file = 'src/instances/groupe2/problem1.pddl'

domain = pddlparser.PDDLParser.parse(domain_file)
problem = pddlparser.PDDLParser.parse(problem_file)


grounder = Grounder(domain, problem)


task = grounder.ground()
# task = grounder.ground()

print(weighted_astar_search(task, heuristic=LandmarkHeuristic(task), weight=5))
