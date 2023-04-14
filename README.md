# pddl_solver
Implemention of a solver which takes as input a domain and a planification problem, and returns a valid plan if some exists.

## Configure the repo to run minisat solver

### Clone minisat repo on your linux system
```git clone https://github.com/agurfinkel/minisat.git```

### Configure the installer
run ```cd minisat``` and then ```make config prefix=/usr``` or ```make config prefix=/usr/local```

### Build the repo and install minisat
run ```sudo make install```.
You should now be able to use minisat (if the directory you set as a prefix is in your path)
