import itertools, random, multiprocessing, time

import usolib
from usolib.helpers import *

N = 4

def main(uso):
    usolib.randomfacet.cache.clear()
    return usolib.randomfacet.randomfacet_analytic(uso, N) / float(factorial(N) * 2**N)


if __name__ == "__main__":
    usos = list(usolib.uso.itr_all(N))
    lst = pmap(main, usos, processes=6)
    res = sum(lst)
    print (res / len(usos))
    print len(usos)

