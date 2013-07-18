
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
    d = dict((q1, set([b])) for (q1, a, b, _) in edges if a == "0")

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
        
            
def is_bosshard(edges):
    # dict of parities
    d = dict((q1, b) for (q1, a, b, _) in edges if a == "0")

    res = set((q1, d[q2]) for (q1, _, _, q2) in edges)
    if len(res) == len(edges):
        return True
    return False


def hopcroft_fingerprint(uso):
    """
    Produce a fingerprint of an uso based on a variant of Hopcroft's algorithm.

    States are first split into even and odd, then iteratively into more refined classes depending on their
    own class and the class of their neighbors. At each point, those classes form an equivalence relation
    on the set of states, and if the transducer is minimal, each state will be in its own class after k-1
    iterations.
    The purpose of the original hopcroft algorithm is to test whether an automaton is minimal. However,
    writing a (size n^2) log of the process according to a standardised format (lexical ordering of classes)
    produces a unique fingerprint for each transducer.
    The only failure mode is when comparing transducers with a different number of states.  This is 
    remedied by rejecting all transducers that are not minimal with a dummy fingerprint (the empty string).
    """
    # initially, separate states by their parities
    class_index = {"+": "0", "-": "1"}
    state_index = dict((q, class_index[uso.table[q, "0"][1]]) for q in uso.states)
    res = [state_index[uso.start_state]]

    for i in range(max(1, uso.k - 1)):
        # assign a class triple to each state, namely the class of the state itself, of its
        # 0-neighbor and of its 1-neighbor
        state_lst = [(q, (state_index[q], state_index[uso.table[q, "0"][0]], state_index[uso.table[q, "1"][0]]))
                     for q in uso.states]

        # find out what classes we have, put them in some canonical order
        # then assign an index to each class (basically a reverse lookup of the list of classes)
        classes = sorted(set(c for (state, c) in state_lst))
        class_index = dict((c, str(i)) for (i,c) in enumerate(classes))

        # assign to each state the index of its class
        state_index = dict((q, class_index[c]) for (q, c) in state_lst)

        # add the result of this iteration to the fingerprint
        res.append(state_index[uso.start_state])
        res.extend("".join(c) for c in classes)

    if len(classes) < uso.k:
        # transducer can be realized with fewer states, return dummy fingerprint
        return ""

    return "".join(res)


def uniq(usos, quiet=False):
    """
    Take an uso iterator, and produce an iterator that filters out repeated usos.
    """
    test = set([""])
    count = 0
    uniq_count = 0
    for uso in usos:
        count += 1
        if (not quiet) and (not count % 1000):
            print "%8d  %8d" % (count, uniq_count)
        fingerprint = hopcroft_fingerprint(uso)
        if fingerprint in test:
            continue
        test.add(fingerprint)
        uniq_count += 1
        yield uso
    if not quiet:
        print "%8d  %8d" % (count, uniq_count)

