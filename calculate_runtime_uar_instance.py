import itertools, random, multiprocessing, time

import usolib

from usolib.helpers import *


def main(n):
    uso = usolib.uso.uar(10)
    lst = [usolib.randomfacet.randomfacet_sample(uso, 20) for i in range(N)]
    return sum(lst) / float(N)


if __name__ == "__main__":
    
    N = 500
    n_usos = 12
    lst = pmap(main, [N for i in range(n_usos)], processes=6)
    print "%.4f" % (sum(lst) / float(n_usos))

