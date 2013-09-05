import time

import usolib
from usolib.helpers import *

def main(n):
    uso = usolib.uso.bad4state()
    return usolib.randomfacet.randomfacet_analytic(uso, n)


if __name__ == "__main__":
    print " n\ttime\tavg"
    for n in range(1, 11):
        t = time.time()
        res = main(n) / float(factorial(n) * 2**n)
        print "%2d\t%.2fs\t%.6f" %(n, time.time() - t, res)

