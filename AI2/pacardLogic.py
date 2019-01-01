import logic

def get_next_literals(problem, literal, state, negative = False):
    x, y = state
    successors = problem.getSuccessors(state)
    ret = list()
    for succ in successors:
        ret.append(logic.Literal(literal, succ[0], negative))
    return ret

def generate_powerset_clauses(literal_groups):

    ret = [[x] for x in literal_groups.pop()]
    while len(literal_groups) > 0:

        group = literal_groups.pop()
        ret2 = list()
        for l in group:
            for ret_group in ret:
                new_g = list(ret_group)
                new_g.append(l)
                ret2.append(new_g)
        ret = ret2
    ret_clauses = list()
    for clause in ret:
        ret_clauses.append(logic.Clause(set(clause)))

    return ret_clauses

def if_sth_then_sth(state, problem, literal_1, literal_2):
    # l1 -> ~l2 <=> ~l1 or ~l2
    s = logic.Literal(literal_1, state, True)
    ret = get_next_literals(problem, literal_2, state)
    ret.append(s)
    return [logic.Clause(ret)]

def if_not_sth_then_not_sth(state, problem, literal_1, literal_2):
    # ~l1 -> ~l2 <=> l1 or ~l2
    s = logic.Literal(literal_1, state)
    r = get_next_literals(problem, literal_2, state, True)
    ret = generate_powerset_clauses([[s], r])
    return ret

def stench(problem, state):
    return if_sth_then_sth(state, problem, 's', 'w')

def no_stench(problem, state):
    return if_not_sth_then_not_sth(state, problem, 's', 'w')

def fume(problem, state):
    return if_sth_then_sth(state, problem, 'b', 'p')

def no_fume(problem, state):
    return if_not_sth_then_not_sth(state, problem, 'b', 'p')

def tele_glow(problem, state):
    return if_sth_then_sth(state, problem, 'g', 't')

def no_tele_glow(problem, state):
    return if_not_sth_then_not_sth(state, problem, 'g', 't')

def wumpus(problem, state):
    return if_sth_then_sth(state, problem, 'w', 'w')

def any_unique(state):
    ret = [logic.Clause([logic.Literal(logic.Labels.WUMPUS, state), logic.Literal(logic.Labels.TELEPORTER, state), logic.Literal(logic.Labels.POISON, state), logic.Literal(logic.Labels.SAFE, state)])]
    return ret

def safe(problem, state):
    g = logic.Literal('g', state)
    s = logic.Literal('s', state)
    b = logic.Literal('b', state)

    nl = get_next_literals(problem, 'o', state)
    return generate_powerset_clauses([[g], [s], [b], nl])
