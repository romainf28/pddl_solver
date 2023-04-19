# pddl_solver

Implemention of a solver which takes as input a domain and a planification problem, and returns a valid plan if some exists.

# Minisat Planner

To run our planner based on minisat, please first make minisat command available to your path

## Configure the repo to run minisat solver

### Clone minisat repo on your linux system to the root of the folder

`git clone https://github.com/agurfinkel/minisat.git`

### Configure the installer

run `cd minisat` and then `make config prefix=/usr` or `make config prefix=/usr/local`

### Build the repo and install minisat

run `sudo make install`.
You should now be able to use minisat (if the directory you set as a prefix is in your path)

### Run the planner on a given instance

from the root, execute `python3 src/sat_solver/main.py --domain_file src/instances/groupe1/domain.pddl --problem_file src/instances/groupe0.pddl`
