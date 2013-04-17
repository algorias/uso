
"""
This script does some analysis on the runtime of pivot elements, 
which are (vertex, facet) pairs passed as arguments in the 2nd recursive call of randomfacet.
"""

import usolib


def xor(x, y):
    return "0" if x == y else "1" 


def flip(w, i):
    """
    Flip the ith dimension of w, i.e. get w ^ {i}, where w is a vertex or a cube.
    """
    return w[:i] + xor(w[i], "1") + w[i+1:]


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



if __name__ == "__main__":
    N = 5
    lst = get_pivots(usolib.fst.bad_uso, "*" * N)

    for i in lst:
        print i

