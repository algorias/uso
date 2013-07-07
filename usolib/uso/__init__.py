import random, itertools

import fst

def ascending():
    """
    Trivial uso with 1...1 as the sink.
    """
    table = {(0, "0"): (0, "-"),
             (0, "1"): (0, "+")}
    return fst.SimpleFST(table)


def bad():
    """
    Very slow uso.
    
    This is not a matousek orientation.
    """
    table = {(0, "0"): (1, "+"),
             (0, "1"): (2, "-"),
             (1, "0"): (2, "-"),
             (1, "1"): (0, "+"),
             (2, "0"): (0, "+"),
             (2, "1"): (1, "-")}
    return fst.SimpleFST(table)


def bad4state():
    """
    Worst 4-state uso, found by tournament.
    """
    edges = [(0, '0', '+', 0),
             (0, '1', '-', 3),
             (1, '0', '+', 3),
             (1, '1', '-', 0),
             (2, '0', '-', 1),
             (2, '1', '+', 2),
             (3, '0', '-', 2),
             (3, '1', '+', 1)]
    return fst.SimpleFST(edges=edges)



def matousek1():
    """
    Matousek uso with a matrix of the form:
        1
        1 1
        0 1 1
        1 0 1 1
        1 1 0 1 1
        0 1 1 0 1 1

    Randomfacet runs slowly on this.
    """
    table = {("start", "0"): ("start", "+"),
             ("start", "1"): ("e2", "-"),
             ("e1", "0"): ("e2", "-"),
             ("e1", "1"): ("start", "+"),
             ("e2", "0"): ("o1", "-"),
             ("e2", "1"): ("e1", "+"),
             ("o1", "0"): ("e1", "+"),
             ("o1", "1"): ("o1", "-")}
    return fst.SimpleFST(table, start="start")


def klee_minty():
    """
    The famous klee-minty cube, which forces many determinstic pivot rules into exponential runtimes.

    This automaton also creates worst case behaviour for RandomFacet: Starting at 0...0, always
    recurse into the smallest available dimension, for a runtime of 2^n. The expected runtime, 
    in constrast, is O(n^2).
    """
    table = {("odd", "0") : ("odd", "+"),
             ("odd", "1") : ("even", "-"),
             ("even", "0") : ("even", "-"),
             ("even", "1") : ("odd", "+")}
    return fst.SimpleFST(table, start="even")

    # another variant
    #table = {("odd", "0") : ("even", "+"),
    #         ("odd", "1") : ("odd", "-"),
    #         ("even", "0") : ("odd", "-"),
    #         ("even", "1") : ("even", "+")}
    #return fst.SimpleFST(table, start="odd")



def random_circle(k):
    """
    Build random uso by taking k states of random parities and linking them together in a circle
    """
    parities = [random.random() > 0.5 for i in range(k)]

    # move clockwise when input is 0, otherwise ccw
    d1 = dict(((state, "0"), ((state+1)%k, "+" if parities[state] else "-")) for state in range(k))
    d2 = dict(((state, "1"), ((state-1)%k, "-" if parities[state] else "+")) for state in range(k))

    d1.update(d2)

    return fst.SimpleFST(d1)
    

def uar(n):
    """
    Build an uso taken uar from USO_id.
    """

    # states are numbered as follows: the root has label 1. Children of node i have labels 2*i and 2*i + 1
    d = {}
    states = xrange(2**(n-1))
    for state in states:
        parity = random.random() > 0.5
        d[(state, "0")] = (2*state, "+" if parity else "-")
        d[(state, "1")] = (2*state + 1, "-" if parity else "+")

    # leaves of tree need to point somewhere
    states = xrange(2**(n-1), 2**n)
    for state in states:
        parity = random.random() > 0.5
        nextstate = random.choice(("asc", "desc"))
        d[(state, "0")] = (nextstate, "+" if parity else "-")
        d[(state, "1")] = (nextstate, "-" if parity else "+")

    d[("asc", "0")] = ("asc", "+")
    d[("asc", "1")] = ("asc", "-")
    d[("desc", "0")] = ("desc", "-")
    d[("desc", "1")] = ("desc", "+")

    return fst.SimpleFST(d, start=1)


def itr_all_by_dim(n):
    """
    Return iterator yielding all regular usos of dimension n.
    """

    for bits in itertools.product([True, False], repeat=2**n-1):
        # states are numbered as follows: the root has label 1. Children of node i have labels 2*i and 2*i + 1
        d = {}
        bits = iter(bits)
        states = range(1, 2**(n-1))
        for state in states:
            parity = next(bits)
            d[(state, "0")] = (2*state, "+" if parity else "-")
            d[(state, "1")] = (2*state + 1, "-" if parity else "+")

        # leaves of tree need to point somewhere
        states = range(2**(n-1), 2**n)
        for state in states:
            parity = next(bits)
            d[(state, "0")] = (1, "+" if parity else "-")
            d[(state, "1")] = (1, "-" if parity else "+")

        yield fst.SimpleFST(d, start=1)



def itr_all_by_states(k):
    """
    Return iterator yielding all regular usos with at most k sates.

    The implementation does not guarantee that an uso won't be returned multiple times.
    """

    if k == 1:
        # special case that doesn't work due to an optimization below
        yield ascending()
        return
    
    states = range(k)
        
    # all possible combinations of 0 transitions
    for lst_0 in itertools.product(states, repeat=len(states)):

        # all possible combinations of 1 transitions
        for lst_1 in itertools.product(states, repeat=len(states)):

            # 0 is always the start state. 
            # states from 0 to j are odd, from j+1 to k-1 they are even
            # the start state is always odd, and there is always at least one even state.
            for j in range(k-1):
            
                # actually generate the uso
                d = {}
                for state in states[:j+1]:
                    # odd states
                    d[(state, "0")] = (lst_0[state], "+")
                    d[(state, "1")] = (lst_1[state], "-")

                for state in states[j+1:]:
                    # even states
                    d[(state, "0")] = (lst_0[state], "-")
                    d[(state, "1")] = (lst_1[state], "+")

                yield fst.SimpleFST(d, start=0)
    

