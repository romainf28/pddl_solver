

if __name__ == '__main__':

    from translate.pddl_parser.pddl_file import open
    from planner.encoder import Encoder

    task = open(
        'instances/groupe3/domain.pddl', 'instances/groupe3/problem1.pddl')

    enc = Encoder(task, horizon=10)
    enc.create_variables()
    print(enc.encode_initial_state().display())
