import time

import usolib
from usolib.helpers import *


def main(n):
    uso = usolib.uso.bad4state()
    return usolib.randomfacet.randomfacet_sample(uso, n)


if __name__ == "__main__":
    print " n\ttime\tavg runtime"
    for n in range(1, 31):
        t = time.time()
        N_samples = 1000
        lst = pmap(main, [n for i in range(N_samples)], processes=6)
        res = sum(lst) / float(N_samples)
        print "%2d\t%4.2fs\t%.6f" %(n, time.time() - t, res)

