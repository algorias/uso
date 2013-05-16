import pprint
from collections import defaultdict

import usolib
from usolib.helpers import *


def get_execution_data(n, uso, cache=None):
    """ execute randomfacet and return cache data"""
    if cache is None:
        cache = {}
    # replace cache with own cache instance
    usolib.randomfacet.cache = cache
    usolib.randomfacet.randomfacet_analytic(uso, n)
    return cache


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
    Accumulate values of dict by keys (or an equivalence relation f on the keys).
    """
    acc = defaultdict(list)
    for (k,v) in d.iteritems():
        acc[f(v)].append(k)
    return acc

def map_vals(d, f):
    """
    Apply f to each value in the dict.
    """
    res = {}
    for (k,v) in d.iteritems():
        res[k] = f(v)
    return res


def main(dim, d, cache):
    # summarise argument pairs by the number of times they were called in total
    by_ncalls = accumulate_keys(d)

    # it's also possible to accumulate results by subcube regardless of the vertex we're at, but the
    # results are not so clear.
    #d = accumulate_by_key(d, lambda (vertex, cube): cube)
    #d = map_vals(d, sum)
    #by_ncalls = accumulate_by_val(d)

    for (k,v) in by_ncalls.items():
        print "%s, %s" %(k, len(v))
        pprint.pprint(v)


if __name__ == "__main__":
    N = 5

    # accumulate data into cache
    cache = CountingDict()
    uso = usolib.uso.bad()
    get_execution_data(N, uso, cache)

    #  
    by_dim = partition(cache.counter, lambda (vertex, subcube), _: get_dimension(subcube))
    by_dim = sorted(by_dim.iteritems())

    # by_dim is list of (dimension, dict) tuples.
    # dicts have same format as get_execution_data

    dim, d = by_dim[N-1]
    main(dim, d, cache)

