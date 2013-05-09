import random

import fst

# trivial uso with 1...1 as the sink
table = {(0, "0"): (0, "-"),
         (0, "1"): (0, "+")}
ascending = fst.SimpleFST(table)


# very slow uso, not a matousek orientation
table = {(0, "0"): (1, "+"),
         (0, "1"): (2, "-"),
         (1, "0"): (2, "-"),
         (1, "1"): (0, "+"),
         (2, "0"): (0, "+"),
         (2, "1"): (1, "-")}
bad = fst.SimpleFST(table)


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
    The famous klee-minty cube.
    """
    table = {("odd", "0") : ("odd", "+"),
             ("odd", "1") : ("even", "-"),
             ("even", "0") : ("even", "-"),
             ("even", "1") : ("odd", "+")}
    return fst.SimpleFST(table, start="odd")



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
    Build an uso taken uar from all recursively combed usos.
    """

    # states are numbered as follows: the root has label 1. Children of node i have labels 2*i and 2*i + 1
    d = {}

    states = xrange(2**(n-1))
    for state in states:
        parity = random.random() > 0.5
        d[(state, "0")] = (2*state, "+" if parity else "-")
        d[(state, "1")] = (2*state + 1, "-" if parity else "+")

    # rightmost states of tree need to point somewhere, loop back for simplicity
    states = xrange(2**(n-1), 2**n)
    for state in states:
        parity = random.random() > 0.5
        d[(state, "0")] = (1, "+" if parity else "-")
        d[(state, "1")] = (1, "-" if parity else "+")

    return fst.SimpleFST(d, start=1)


# clean up namespace
del table

