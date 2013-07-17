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
    K = 4
    usos_itr = usolib.uso.all_by_states(K)
    fd = open("/home/vitor/usos.txt", "w")
    test_set = set()
    count = 0
    raw_count = 0

    for uso in usos_itr:
        raw_count += 1
        if not raw_count % 1000:
            print "%8d  %8d" % (raw_count, count)

        fingerprint = uso.fingerprint(2*K - 1)
        if fingerprint in test_set:
            continue
        test_set.add(fingerprint)
        for i in uso.get_edges():
            print >> fd, i
        print >> fd
        count += 1

    print "%7d  %7d" % (raw_count, count)
    
