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


def print_statistic(usos):
    avg = average([runtime for (runtime, uso) in usos])
    mx = max(runtime for (runtime, uso) in usos)
    print "avg runtime: %s" % avg
    print "max runtime: %s" % usos[-1][0]
    print "min runtime: %s" % usos[0][0]

    print "slowest candidate:"
    for i in usos[-1][1].get_edges():
        print i

    print


if __name__ == "__main__":
    K = 5
    #usos_itr = usolib.uso.all_by_states(K)
    usos_itr = usolib.uso.all_bosshard(K)
    usos = list(usolib.uso.fst.uniq(usos_itr, 2*K - 1))

    for N in range(8, 39, 2):
        print "N=%s" % N
        print "testing %d usos" % len(usos)
        t = time.time()
        lst = pmap(runtime_sampled, usos, processes=6, args=(N,))
        print "finished in %d seconds" % (time.time() - t)

        lst = sorted(lst)
        print_statistic(lst)
        lst = lst[-int(len(lst)*0.5):]
        usos = [uso for (runtime, uso) in lst]

    print "all survivors:"
    for uso in usos:
        for i in uso.get_edges():
            print i
        print


