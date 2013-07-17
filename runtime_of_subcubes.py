import pprint
from collections import defaultdict

import usolib
from usolib.helpers import *


def partition(d, f):
    """ 
    Partition entries in dict d by function f, which takes a key and a value as input.
    """
    res = defaultdict(dict)
    for (k, v) in d.iteritems():
        res[f(k,v)][k] = v
    return res


def accumulate_vals(d, f=lambda x: x):
    """
    Accumulate values of dict by keys (or an equivalence relation f on the keys).
    """
    acc = defaultdict(list)
    for (k,v) in d.iteritems():
        acc[f(k)].append(v)
    return acc


def accumulate_keys(d, f=lambda x: x):
    """
    Accumulate keys of dict by keys (or an equivalence relation f on the keys).
    """
    acc = defaultdict(list)
    for (k,v) in d.iteritems():
        acc[f(v)].append(k)
    return acc

def map_vals(d, f):
    """
    Apply f to each value in the dict.
    """
    return dict((k, f(v)) for (k,v) in d.iteritems())



def main(dim, d):
    d = accumulate_vals(d, lambda (vertex, subcube): subcube)
    d = map_vals(d, sum)
    c = defaultdict(int)
    for v in d.itervalues():
        c[v] += 1

    for i in sorted(c.items(), key = lambda (runtime, count): count):
        print i


if __name__ == "__main__":
    N = 5

    # accumulate data into cache
    cache = {}
    cache = CountingDict()
    uso = usolib.uso.bad4state()
    usolib.randomfacet.randomfacet_analytic(uso, N, cache=cache)

    #  
    by_dim = partition(cache.counter, lambda (vertex, subcube), _: get_dimension(subcube))
    by_dim = sorted(by_dim.iteritems())

    for dim, d in by_dim:
        print dim
        print len(d)
        main(dim, d)
        print



