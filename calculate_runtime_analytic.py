import itertools, random, multiprocessing, time
from itertools import product

import usolib
from usolib.helpers import *


def main(n, step, start):
    uso = usolib.uso.bad()
    vertices = generate_vertices(n, start, step)
    return usolib.randomfacet.randomfacet_analytic(uso, n, vertices)


if __name__ == "__main__":
    n_processes = 6

    print " n\ttime\tavg"
    for n in range(1, 11):
        t = time.time()
        lst = pmap(main, range(n_processes), n_processes, args=(n, n_processes))
        res = sum(lst) / float(factorial(n) * 2**n)
        #res = max(lst) / float(factorial(n))
        print "%2d\t%.2fs\t%.4f" %(n, time.time() - t, res)

