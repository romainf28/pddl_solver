from sat_planner import SATPlanner
import itertools

domain_file = '../instances/groupe2/domain.pddl'
problem_file = '../instances/groupe2/problem1.pddl'

planner = SATPlanner(domain_file, problem_file)
plan = planner.find_plan(min_horizon=1, max_horizon=10)

# print(plan)

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
