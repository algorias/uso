import itertools, random, multiprocessing, time

import usolib

from usolib.helpers import *


def main(n):
    uso = usolib.uso.bad()
    return usolib.randomfacet.randomfacet_sample(uso, n)


if __name__ == "__main__":
    
    print " n\ttime\tavg runtime"
    for n in range(1, 21):
        t = time.time()
        N = 1000
        lst = pmap(main, [n for i in range(N)], processes=6)
        res = sum(lst) / float(N)
        print "%2d\t%4.2fs\t%.4f" %(n, time.time() - t, res)

