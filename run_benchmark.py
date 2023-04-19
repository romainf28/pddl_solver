planners_config = {
    "groupe1": {
        "problem0.pddl": "python3 src/sat_planner/main.py --domain_file src/instances/groupe1/domain.pddl --problem_file src/instances/groupe1/problem0.pddl --min_horizon 1 --max_horizon 10",
        "problem1.pddl": "python3 src/heuristics/main.py --domain_file src/instances/groupe1/domain.pddl --problem_file src/instances/groupe1/problem1.pddl"
    },
    "groupe2": {
        "problem0.pddl": "python3 src/sat_planner/main.py --domain_file src/instances/groupe2/domain.pddl --problem_file src/instances/groupe2/problem0.pddl  --min_horizon 1 --max_horizon 10",
        "problem1.pddl": "python3 src/sat_planner/main.py --domain_file src/instances/groupe2/domain.pddl --problem_file src/instances/groupe2/problem1.pddl  --min_horizon 1 --max_horizon 10",
        "problem2.pddl": "python3 src/sat_planner/main.py --domain_file src/instances/groupe2/domain.pddl --problem_file src/instances/groupe2/problem2.pddl  --min_horizon 1 --max_horizon 30"
    },
    "groupe3": {
        "problem1.pddl": "python3 src/heuristics/main.py --domain_file src/instances/groupe3/domain.pddl --problem_file src/instances/groupe3/problem1.pddl --partial_grounding 1"
    },
    "groupe4": {
        "probfreecell-2-3.pddl": "python3 src/heuristics/main.py --domain_file src/instances/groupe4/domain.pddl --problem_file src/instances/groupe4/probfreecell-2-3.pddl",
        "probfreecell-3-5.pddl": "python3 src/heuristics/main.py --domain_file src/instances/groupe4/domain.pddl --problem_file src/instances/groupe4/probfreecell-3-5.pddl",
        "probfreecell-5-3.pddl": "python3 src/heuristics/main.py --domain_file src/instances/groupe4/domain.pddl --problem_file src/instances/groupe4/probfreecell-5-3.pddl",
    }
}


if __name__ == '__main__':
    import os
    import time
    for group, problems in planners_config.items():
        for problem, command in problems.items():
            print(f"Solving {problem} of {group}")
            t0 = time.time()
            os.system(command)
