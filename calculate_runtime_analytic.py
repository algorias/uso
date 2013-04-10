import itertools, random, multiprocessing, time
from itertools import product

import usolib
from usolib.helpers import *


def main((start, step, n)):
    return usolib.randomfacet.randomfacet_analytic(usolib.fst.bad_uso, n, generate_vertices(n, start, step))


if __name__ == "__main__":
    n_processes = 6
    pool = multiprocessing.Pool(processes=n_processes)
    
    print " n\ttime\tavg"
    for n in range(11, 16):
        t = time.time()

        async_result = pool.map_async(main, ((i, n_processes, n) for i in range(n_processes)))
        while not async_result.ready():
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                pool.terminate()
                pool.join()
                exit()
        lst = async_result.get()
        res = sum(lst) / float(factorial(n) * 2**n)
        print "%2d\t%.2fs\t%.4f" %(n, time.time() - t, res)

