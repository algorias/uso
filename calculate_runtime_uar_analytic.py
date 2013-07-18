import time

import usolib
from usolib.helpers import *

N = 3

def main(uso):
    return usolib.randomfacet.randomfacet_analytic(uso, N, cache={}) / float(factorial(N) * 2**N)


if __name__ == "__main__":
    usos = list(usolib.uso.all_by_dim(N))
    lst = pmap(main, usos, processes=6)
    res = sum(lst)
    print (res / len(usos))
    print len(usos)

