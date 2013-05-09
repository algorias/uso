
"""
This script does some analysis on the runtime of pivot elements, 
which are (vertex, facet) pairs passed as arguments in the 2nd recursive call of randomfacet.
"""
import random, itertools

import usolib
from usolib.helpers import *


def flip(w, i):
    """
    Flip the ith dimension of w, i.e. get w ^ {i}, where w is a vertex or a cube.
    """
    return w[:i] + ("1" if w[i] == "0" else "0") + w[i+1:]


def split(cube, side, i):
    """
    Split cube along dimension i, and return correct side.
    """
    return cube[:i] + side + cube[i+1:]



def get_pivot(uso, cube, i):
    sink = uso.find_sink(cube)
    goodfacet = split(cube, sink[i], i)
    badfacet = flip(goodfacet, i)
    vertex = flip(uso.find_sink(badfacet), i)
    return vertex, goodfacet
    

def get_pivots(uso, cube):
    return [get_pivot(uso, cube, i) 
            for i in range(len(cube)) 
            if cube[i] == "*"]


def main((vertex, facet)):
    return usolib.randomfacet.randomfacet_sample(uso, N, cube=facet, vertex=vertex) 


if __name__ == "__main__":
    uso = usolib.uso.bad()
    n_processes = 6
    n_samples = 100

    for N in range(101, 151):
        # sample as uniformly as possible
        lst = get_pivots(uso, "*" * N)
        random.shuffle(lst)
        itr = itertools.cycle(lst)
        lst = [next(itr) for i in range(n_samples)]

        res = pmap(main, lst, processes=n_processes)

        print "%4d %4.2f" %(N, sum(res) / float(n_samples))


