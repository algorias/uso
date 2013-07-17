
def reachable_states(edges, start=0):
    """
    Given a set of edges and a start state, return list of reachable states.
    """
    reach = set([start])
    k = len(edges) / 2
    for i in range(k - 1):
        reach.update(q2 for (q1, a, b, q2) in edges if q1 in reach)
    return reach


def redundant_states(edges):
    """
    Given a set of edges, find states that are unneeded.
    """
    # initialize every state with its own parity
    d = dict((q1, set([b])) for (q1, a, b, q2) in edges if a == "0")

    # iteratively update reachable parities for each state
    k = len(edges) / 2
    for i in range(k - 1):
        for (q1, a, b, q2) in edges:
            d[q1].update(d[q2])

    # If a state reaches only its own parities, it might be redundant.
    maybe_redundant = set(q for (q, reach) in d.iteritems() if len(reach) < 2)
    redundant = set()

    # If state is trivial, it's ok. If not, we have proof that fst is not minimal.
    for (q1, a, b, q2) in edges:
        if q1 in maybe_redundant and q1 != q2:
            redundant.add(q1)
    return redundant


def minimal_heuristic(edges):
    """
    Half-heuristic to determine whether a fst has a representation with less states.
    False positives are possible, false negatives aren't.

    if False: we're 100% sure that it's NOT a minimal realization of that transducer
    If True: maybe minimal, maybe not.
    """
    k = len(edges) / 2
    if len(reachable_states(edges)) < k:
        return False
    if len(redundant_states(edges)):
        return False
    return True
        
            

