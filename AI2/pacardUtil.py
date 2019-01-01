from logic import *
import pacardLogic

def is_label_in_state(state, resolved_states, labels):

    for l in labels:
        if Clause(Literal(l, state)) in resolved_states:
            return True
    return False

def neighbouring_something(state, problem, resolvedStates, labels):

    ret_states = set()
    successors = problem.getSuccessors(state)
    for succ in successors:
        for l in labels:
            if is_label_in_state(succ[0], resolvedStates, l):
                ret_states.add(succ)
    return ret_states

def add_succs_tele(states, current_state, problem, resolved, visited_states):

    successors = neighbouring_something(current_state, problem, resolved, Labels.TELEPORTER)
    for succ in successors:
        if succ[0] not in visited_states:
            states.push(succ[0], 1)

def add_succs_safe(states, current_state, problem, resolved, visited_states):

    successors = neighbouring_something(current_state, problem, resolved, Labels.SAFE)
    for succ in successors:
        if succ[0] not in visited_states:
            states.push(succ[0], 1)

def add_succs_unknown(states, current_state, problem, resolved, visited_states):

    succs = problem.getSuccessors(current_state)

    for succ in succs:
        if not is_label_in_state(succ[0], resolved, Labels.UNIQUE):
            if succ[0] not in visited_states:
                states.push(succ[0], 1)

def first_state_from_queues(list_of_queues, resolved, visited):

    for i in range(3):
        queue = list_of_queues[i]
        while not queue.isEmpty():
            ret = queue.pop()
            if not is_label_in_state(ret, resolved, Labels.DEADLY) and not ret in visited:
                return ret

def get_info(state, problem):

    info = set()

    if problem.isWumpusClose(state):
        info.add(Labels.WUMPUS_STENCH)

    if problem.isWumpus(state):
        info.add(Labels.WUMPUS)

    if problem.isTeleporterClose(state):
        info.add(Labels.TELEPORTER_GLOW)

    if problem.isTeleporter(state):
        info.add(Labels.TELEPORTER)

    if problem.isPoisonCapsule(state):
        info.add(Labels.POISON)

    if problem.isPoisonCapsuleClose(state):
        info.add(Labels.POISON_FUMES)

    return info

def find_suitable_indicator(label):

    if label == Labels.POISON_FUMES:
        return Labels.POISON

    if label == Labels.TELEPORTER_GLOW:
        return Labels.TELEPORTER

    if label == Labels.WUMPUS_STENCH:
        return Labels.WUMPUS

    print "about to do something bad"
    return None

def give_info_to_state(current_state, problem, resolvedStates):

    state_info = get_info(current_state, problem)
    successors = problem.getSuccessors(current_state)

    new_resolvents = set()
    just_to_be_safe_set = set(Labels.INDICATORS)
    for l in just_to_be_safe_set.union(Labels.WTP):
        if l in state_info:
            new_resolvents.add(Clause(Literal(l, current_state, False)))
        else:
            new_resolvents.add(Clause(Literal(l, current_state, True)))

    for l in Labels.INDICATORS:
        if l not in state_info:
            for succ in successors:
                ind = find_suitable_indicator(l)
                new_resolvents.add(Clause(Literal(ind, succ[0], True)))

    return new_resolvents

def generate_new_clauses(current_state, problem):
    successors = problem.getSuccessors(current_state)
    plg = pacardLogic
    new_clauses = set()

    new_clauses.update(set(plg.tele_glow(problem, current_state)))
    new_clauses.update(set(plg.no_tele_glow(problem, current_state)))

    new_clauses.update(set(plg.stench(problem, current_state)))
    new_clauses.update(set(plg.no_stench(problem, current_state)))

    new_clauses.update(set(plg.fume(problem, current_state)))
    new_clauses.update(set(plg.no_fume(problem, current_state)))

    new_clauses.update(set(plg.safe(problem, current_state)))
    new_clauses.update(set(plg.any_unique(current_state)))

    for succ in successors:
        current_state = succ[0]
        new_clauses.update(set(plg.safe(problem, current_state)))
        new_clauses.update(set(plg.any_unique(current_state)))
    return new_clauses

def conclude_successors(problem, current_state, resolved, known_clauses, unknown_states):

    successors = problem.getSuccessors(current_state)

    for state in successors:
        for l in Labels.UNIQUE:
            goal = Clause(Literal(l, state[0]))
            res = resolution(known_clauses, goal)
            if res:
                resolved.add(Clause(Literal(l, state[0])))

    for entry in unknown_states.items():
        print "ENTRY IN UTIL: ", entry
        for l in Labels.UNIQUE:
            goal = Clause(Literal(l, entry))
            res = resolution(known_clauses, goal)
            if res:
                resolved.add(Clause(Literal(l, entry)))

    return resolved
