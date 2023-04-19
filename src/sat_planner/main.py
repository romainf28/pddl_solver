from sat_planner import SATPlanner

if __name__ == '__main__':
    import argparse
    import time
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--domain_file", help="path to the pddl domain file", required=True)
    parser.add_argument(
        "--problem_file", help="path to the pddl problem file", required=True)
    parser.add_argument(
        "--min_horizon", help="start horizon for the planner", required=False, default=1)
    parser.add_argument(
        "--max_horizon", help="end horizon for the planner", required=False, default=20)
    parser.add_argument(
        "--output_file", help="path to the file to store the outputs", default="benchmark_results.txt")
    args = parser.parse_args()

    f = open(args.output_file, 'a')
    print('Using SAT planner ... ')
    print('Using SAT solver', file=f)
    t0 = time.time()
    planner = SATPlanner(args.domain_file, args.problem_file)
    plan = planner.find_plan(min_horizon=int(args.min_horizon),
                             max_horizon=int(args.max_horizon))
    if plan:
        print('A plan was found. Ellapsed time : {}'.format(time.time()-t0))
        print('A plan was found. Ellapsed time : {}'.format(
            time.time()-t0), file=f)
        print('Oprerators of the plan : ')
        state = planner.task.initial_state
        for op in plan:
            print(op)
            print(op, file=f)
            print("========================================================",
                  file=f)
            print("\n", file=f)
            if op.applicable(state):
                state = op.apply(state)

        assert planner.task.goals.issubset(state), "non valid solution"
