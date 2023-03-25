def apply_action(state, action):
    '''
    Applies an action if possible and returns false otherwise
    '''
    if is_applicable(state, action.positive_preconditions, action.negative_preconditions):
        state = state.union(action.add_effects, action.del_effects)
    else:
        return False


def is_applicable(state, positive_preconditions, negative_preconditions):
    '''
    Check whether an action is applicable or not in the current state by looking at the positive and negative preconditions
    '''
    return positive_preconditions.issubset(state) and negative_preconditions.isdisjoint(state)


def get_static_and_dynamic_preidcates(predicates, actions):
    '''
    Splits predicates into dynamic predicates (ie predicates whihch appear in the effects of an action) and
    static predicates (ie predicates which truth value does not change through time)
    '''
    static_predicates = []
    dynamic_predicates = []
    for pred in predicates:
        dynamic = False
        for action in actions:
            for pos_effect in action.add_effects:
                if pos_effect[0] == pred:
                    dynamic = True
                    break
            for neg_effect in action.del_effects:
                if neg_effect[0] == pred:
                    dynamic = True
                    break
        if dynamic:
            dynamic_predicates.append(pred)
        else:
            static_predicates.append(pred)
    return static_predicates, dynamic_predicates


def get_timeless_truth(initial_state, static_predicates):
    '''
    Returns a list of static predicates which are true in the initial state and therefore will remain true throughout execution
    '''
    timeless_truth = []
    for pred in initial_state:
        if pred[0] in static_predicates:
            timeless_truth.append(pred)
    return timeless_truth


def check_positive_preconditions(groundified_action, static_predicates, timeless_truth):
    for positive_precond in groundified_action.positive_preconditions:
        if positive_precond[0] in static_predicates and positive_precond not in timeless_truth:
            return False
    return True


def check_negative_preconditions(groundified_action, static_predicates, timeless_truth):
    for negative_precond in groundified_action.negative_preconditions:
        if negative_precond[0] in static_predicates and negative_precond in timeless_truth:
            return False
    return True


def check_action_parameters(groundified_action):
    parameters = []
    for param in groundified_action.parameters:
        if param not in parameters:
            parameters.append(param)
        else:
            return False
    return True


def predicate_to_string(predicate):
    return '.'.join(predicate)
