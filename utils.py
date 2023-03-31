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


def get_static_and_dynamic_predicates(predicates, actions):
    '''
    Splits predicates into dynamic predicates (ie predicates whihch appear in the effects of an action) and
    static predicates (ie predicates which truth value does not change through time)
    '''
    static_predicates = []
    dynamic_predicates = []
    action_predicates = set()
    for action in actions:
        action_predicates.update(p[0] for p in action.add_effects)
        action_predicates.update(p[0] for p in action.del_effects)
    for pred in predicates:
        if pred in action_predicates:
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
    '''
    Checks if all positive preconditions of a groundified action are static predicates which were satisfied in the initial state
    '''
    for positive_precond in groundified_action.positive_preconditions:
        if positive_precond[0] in static_predicates and positive_precond not in timeless_truth:
            return False
    return True


def check_negative_preconditions(groundified_action, static_predicates, timeless_truth):
    '''
    Checks if all negative preconditions of a groundified action are static predicates which were not satisfied in the initial state
    '''
    for negative_precond in groundified_action.negative_preconditions:
        if negative_precond[0] in static_predicates and negative_precond in timeless_truth:
            return False
    return True


def check_action_parameters(groundified_action):
    '''
    Checks if a groundified action has duplicate parameters
    '''
    parameters = []
    for param in groundified_action.parameters:
        if param not in parameters:
            parameters.append(param)
        else:
            return False
    return True


def predicate_to_string(predicate):
    '''
    Converts a predicate to a more convenient string representation 
    '''
    return '.'.join(predicate)


def action_to_string(action):
    '''
    Converts an action to a more convenient string representation
    '''
    return action.name + '.' + '.'.join(action.parameters)
