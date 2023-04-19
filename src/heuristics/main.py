
from src.heuristics.weighted_astar import weighted_astar_search
from src.grounder import Grounder
import src.pddlparser as pddlparser
from src.heuristics.landmarks import LandmarkHeuristic

if __name__ == '__main__':
    import argparse
    import time
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--domain_file", help="path to the pddl domain file", required=True)
    parser.add_argument(
        "--problem_file", help="path to the pddl problem file", required=True)
    parser.add_argument("--partial_grounding",
                        help="whether to use or not partial grounding", default=0)
    parser.add_argument(
        '--weight', help="weight used in weighted A* search, default to 5", default=5)
    parser.add_argument(
        "--output_file", help="path to the file to store the outputs", default="benchmark_results.txt")
    args = parser.parse_args()

    f = open(args.output_file, 'w')
    print('Using A* planner with landmarks heuristic ... ')
    print('Using A* planner with landmarks heuristic', file=f)
    t0 = time.time()
    domain = pddlparser.PDDLParser.parse(args.domain_file)
    problem = pddlparser.PDDLParser.parse(args.problem_file)
    grounder = Grounder(domain, problem)

    if args.partial_grounding:
        print('Using partial grounding')
        task = grounder.rubiks_partial_grounding()
    else:
        print('Using classical grounding')
        task = grounder.ground()

    plan = weighted_astar_search(
        task, heuristic=LandmarkHeuristic(task), weight=5)
    if plan:
        print('A plan was found. Ellapsed time : {}'.format(time.time()-t0))
        print('A plan was found. Ellapsed time : {}'.format(
            time.time()-t0), file=f)
        print('Oprerators of the plan : ')
        for op in plan:
            print(op)
            print(op, file=f)
            print("========================================================",
                  file=f)
            print("\n", file=f)
