import os
import sys
import subprocess


class CnfHandler:
    def __init__(self, input_file='input.cnf', output_file='output.txt'):
        self.input_file = input_file
        self.output_file = output_file

    def write(self, formula):
        """ Writes a formula to a cnf input file that will be fed to minisat"""
        self.count = 1
        self.vars_to_indices = {}

        aux_iff_vars = set()
        self.cnf_file = open(self.input_file, 'w')

        while formula:

            disjunction = formula.pop(0)
            if not isinstance(disjunction, list):
                self._write_clause([disjunction])
                continue
            new_clause = []
            for conjunction in disjunction:

                if not isinstance(conjunction, list):
                    new_clause.append(conjunction)
                    continue
                # auxiliary vars for iffs
                for literal in conjunction:
                    if '<->' in literal and literal not in aux_iff_vars:
                        self._write_clauses(self._get_aux_clauses_for_iff(
                            literal))
                        aux_iff_vars.add(literal)
                # Turn list into a literal and add auxiliary clauses
                while len(conjunction) > 1:
                    left = conjunction.pop(0)
                    right = conjunction.pop(0)
                    aux_var, clauses = self._get_aux_clauses_for_and(left,
                                                                     right)
                    conjunction.insert(0, aux_var)
                    self._write_clauses(clauses)
                assert len(conjunction) == 1, conjunction
                new_clause.append(conjunction[0])
            self._write_clause(new_clause)

        self.cnf_file.close()
        for var in list(self.vars_to_indices):
            if '<->' in var:
                del self.vars_to_indices[var]
        return self.vars_to_indices

    def _literal_to_index(self, literal):
        if type(literal) is int:
            return literal
        negated = literal.startswith("not-")
        if negated:
            # remove the 'not-'
            literal = literal[4:]
        if literal in self.vars_to_indices:
            idx = self.vars_to_indices[literal]
        else:
            self.count += 1
            idx = self.count
            self.vars_to_indices[literal] = idx
        if negated:
            idx = -idx
        return idx

    def _write_clause(self, clause):
        print(' '.join([str(self._literal_to_index(literal))
              for literal in clause]) + ' 0', file=self.cnf_file)

    def _write_clauses(self, clauses):
        for clause in clauses:
            self._write_clause(clause)

    def _get_aux_clauses_for_iff(self, iff):
        left, right = iff.split('<->')
        return [[iff, left, right],
                [iff, 'not-'+left, 'not-'+right],
                ['not-'+iff, left, 'not-'+right],
                ['not-'+iff, 'not-'+left, right]]

    def _get_aux_clauses_for_and(self, left, right):
        self.count += 1
        aux_var = self.count
        if type(left) is str:
            if left.startswith('not-'):
                not_left = left[4:]
            else:
                not_left = 'not-'+left
        else:
            not_left = -left

        if type(right) is str:
            if right.startswith('not-'):
                not_right = right[4:]
            else:
                not_right = 'not-'+right
        else:
            not_right = -right
        return aux_var, [[-aux_var, left], [-aux_var, right], [not_left, not_right, aux_var]]

    def decode_output(self, names_to_indices):
        """
        Transform the outputs of minisat back into
        the text-variable-names required by our planer.
        """

        indices_to_names = dict()
        for name, idx in names_to_indices.items():
            indices_to_names[idx] = name

        decoded = []

        with open(self.output_file, 'r') as file:
            lines = file.readlines()
        if lines[0].startswith('SAT'):
            vars = lines[1].split()
            # the last element of a line is always a 0
            for var in vars[:-1]:
                negation = ''
                if var.startswith('-'):
                    negation = 'not-'
                    var = var[1:]
                var = indices_to_names.get(int(var))

                if var:
                    decoded.append(negation + var)
        try:
            os.remove(self.output_file)
        except OSError:
            pass
        return decoded


class MinisatSolver:
    def __init__(self, input_file='input.cnf', output_file='output.txt'):
        self.input_file = input_file
        self.output_file = output_file

    def _solve_minisat(self):
        """
        Calls minisat with the specified formula, the number of variables
        and the number of clauses.
        Returns the output filename of the minisat computation.
        """
        try:
            process = subprocess.Popen(['minisat', self.input_file, self.output_file],
                                       stderr=subprocess.PIPE,
                                       stdout=subprocess.PIPE)
            process.wait()
        except OSError:
            print('minisat could not be found. '
                  )

            sys.exit(1)
        try:
            os.remove(self.input_file)
        except OSError:
            pass

    def solve(self, formula):
        """
        Transforms the formula into the format required by minisat, feed the transformed
        formula to minisat and decodes the output of minisat.
        If the formula is satisfiable, a list of variables is returned.
        If the formula is unsatisfiable, an empty list is returned.
        """

        cnf_handler = CnfHandler(self.input_file, self.output_file)
        vars_to_indices = cnf_handler.write(formula)
        self._solve_minisat()
        valuation = cnf_handler.decode_output(vars_to_indices)
        return valuation
