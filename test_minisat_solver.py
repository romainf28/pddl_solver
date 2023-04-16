from sat_planner import SATPlanner
import itertools

domain_file = 'instances/groupe1/domain.pddl'
problem_file = 'instances/groupe1/problem1.pddl'


def rubik_custom_assigner(possible_assignments):

    combs = itertools.product(*possible_assignments[0:0+3])

    unique_combs = set()
    for comb in combs:
        if len(set([color[1] for color in comb])) == 3:
            unique_combs.add(comb)
    print(len(unique_combs))

    assignments = itertools.chain((itertools.combinations(
        possible_assignments[i:i+3], 3) for i in range(0, len(possible_assignments), 3)))
    return assignments


planner = SATPlanner(domain_file, problem_file)
plan = planner.find_plan(min_horizon=15, max_horizon=20)

print(plan)

'''
Results

groupe 1 :

- problem 0 : plan with 6 actions
- problem 1 :

groupe 2:
- problem 0 : plan with 7 actions
- problem 1 : plan with 9 actions
- problem 2 : plan with 20 actions

groupe 3:


groupe 4:
- prob-2-3 : 
'''
