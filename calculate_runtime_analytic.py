import itertools, random, multiprocessing, time
from itertools import product

import usolib
from usolib.helpers import *


def main((start, step, n)):
    uso = usolib.uso.bad
    vertices = generate_vertices(n, start, step)
    return usolib.randomfacet.randomfacet_analytic(uso, n, vertices)


if __name__ == "__main__":
    n_processes = 6

    print " n\ttime\tavg"
    for n in range(1, 11):
        t = time.time()
        lst = pmap(main, ((i, n_processes, n) for i in range(n_processes)), n_processes)
        res = sum(lst) / float(factorial(n) * 2**n)
        print "%2d\t%.2fs\t%.4f" %(n, time.time() - t, res)

