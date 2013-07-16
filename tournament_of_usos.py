import itertools, random, multiprocessing, time
from functools import partial

import usolib
from usolib.helpers import *


def runtime_sampled(N, uso):
    n_samples = 200
    lst = [usolib.randomfacet.randomfacet_sample(uso, N) for i in range(n_samples)]
    return sum(lst) / float(n_samples), uso


def runtime_analytic(N, uso):
    #return uso, usolib.randomfacet.randomfacet_analytic(uso, N, cache={})
    return usolib.randomfacet.randomfacet_analytic(uso, N, cache={}) / float(factorial(N) * 2**N), uso



def filter_usos(usos, N):
    """
    Take a list of (uso, runtime) tuples and filters out those faster than bad on this dimension.
    """
    threshold = runtime_analytic(N, usolib.uso.bad())[1]
    return [(uso, runtime) for (uso, runtime) in usos if runtime >= threshold]


if __name__ == "__main__":
    K = 3
    usos_itr = usolib.uso.itr_all_by_states(K)
    usos = usolib.uso.fst.uniq(usos_itr, 2*K - 1)

    for N in range(4, 21, 2):
        t = time.time()
        lst = pmap(runtime_sampled, usos, processes=6, args=(N,))
        lst = sorted(lst)[-int(len(lst)*0.5):]
        usos = [uso for (runtime, uso) in lst]
        print "N=%d  %ds  %d usos" % (N, time.time() - t, len(usos))
        print "best candidate:"
        for i in usos[-1].get_edges():
            print i
        print

    for uso in usos:
        for i in uso.get_edges():
            print i
        print


