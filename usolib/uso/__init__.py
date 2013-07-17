import random, itertools

import fst
from usolib.graph_helpers import *

def descending():
    """
    Trivial uso with 0...0 as the sink.
    """
    edges = [(0, "0", "+", 0),
             (0, "1", "-", 0)]
    return fst.SimpleFST(edges=edges)


def bad():
    """
    Very slow uso.
    
    This is not a matousek orientation.
    """
    edges = [(0, "0", "+", 1),
             (0, "1", "-", 2),
             (1, "0", "-", 2),
             (1, "1", "+", 0),
             (2, "0", "+", 0),
             (2, "1", "-", 1)]
    return fst.SimpleFST(edges = edges)


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
    edges = [("start", "0", "+", "start"),
             ("start", "1", "-", "e2"),
             ("e1", "0", "-", "e2"),
             ("e1", "1", "+", "start"),
             ("e2", "0", "-", "o1"),
             ("e2", "1", "+", "e1"),
             ("o1", "0", "+", "e1"),
             ("o1", "1", "-", "o1")]

    return fst.SimpleFST(edges=edges, start="start")


def klee_minty():
    """
    The famous klee-minty cube, which forces many determinstic pivot rules into exponential runtimes.

    This automaton also creates worst case behaviour for RandomFacet: Starting at 0...0, always
    recurse into the smallest available dimension, for a runtime of 2^n. The expected runtime, 
    in constrast, is O(n^2).
    """
    edges = [("odd", "0", "+", "odd"),
             ("odd", "1", "-", "even"),
             ("even", "0", "-", "even"),
             ("even", "1", "+", "odd")]
    return fst.SimpleFST(edges=edges, start="even")


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


def all_by_dim(n):
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


def all_by_states(k):
    """
    Return iterator yielding all regular usos with at most k sates.

    The implementation does not guarantee that an uso won't be returned multiple times.
    """
    if k == 1:
        # special case that doesn't work due to an optimization below
        yield descending()
        return

    for uso in all_by_states(k-1):
        yield uso
    
    # 0 is always the start state. 
    # states from 0 to j are odd, from j+1 to k-1 they are even
    # the start state is always odd, and there is always at least one even state.
    for n_odd in range(1, k):
        for i in _itr_states_parity(k, n_odd):
            yield i
    

def _itr_states_parity(k, n_odd):
    """
    Helper function for all_by_states.
    """
    available_edges = []
    for state in range(n_odd):
        available_edges.append((state, "0", "+"))
        available_edges.append((state, "1", "-"))
    for state in range(n_odd, k):
        available_edges.append((state, "0", "-"))
        available_edges.append((state, "1", "+"))

    for uso in _itr_edgeset(k, available_edges):
        yield uso


def _itr_edgeset(k, edges):
    states = range(k)
    states_set = set(states[1:])

    for to_states in itertools.product(states, repeat=2*k):
        lst = [(q1, a, b, q2) for ((q1, a, b), q2) in zip(edges, to_states)]
        if not minimal_heuristic(lst):
            # fst was already realized with less states
            continue
        yield fst.SimpleFST(edges=lst)

