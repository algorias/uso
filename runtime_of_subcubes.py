import pprint
from collections import defaultdict

import usolib


def get_execution_data(n, uso, cache=None):
    """ execute randomfacet and return cache data"""
    if cache is None:
        cache = {}
    # replace cache with own cache instance
    usolib.randomfacet.cache = cache
    usolib.randomfacet.randomfacet_analytic(uso, n)
    return cache


def accumulate_to_subcubes(d):
    """
    Average the runtime of a subcube over all starting positions.
    
    d is the execution data
    """
    acc = defaultdict(int) # sum of runtime
    for ((vertex, cube), (runtime, sink)) in d.iteritems():
        #runtime = runtime_fac / usolib.helpers.factorial(cube.count("*"))
        acc[cube] += runtime

    res = {}
    for cube, runtime in acc.iteritems():
        n = cube.count("*")
        res[cube] = runtime / float(usolib.helpers.factorial(n) * 2**n)

    return res


def partition(d, f):
    """ 
    Partition entries in dict d by function f, which takes a key and a value as input.
    """
    res = defaultdict(dict)
    for (k, v) in d.iteritems():
        res[f(k,v)][k] = v
    return res


def accumulate_by_keys(d, f=lambda x: x):
    acc = defaultdict(list)
    for (k,v) in d.iteritems():
        acc[f(k)].append(v)
    return acc


def accumulate_by_values(d, f=lambda x: x):
    acc = defaultdict(list)
    for (k,v) in d.iteritems():
        acc[f(v)].append(k)
    return acc


def get_dimension((vertex, subcube), _):
    return subcube.count("*")



def main(N, d):
    print
    print "------------ %s ------------" % N
    print

    subcube_runtimes = accumulate_to_subcubes(d)
    by_runtime = accumulate_by_values(subcube_runtimes)
    by_runtime = sorted(by_runtime.iteritems())
    pprint.pprint(by_runtime)



if __name__ == "__main__":
    N = 6
    data = get_execution_data(N, usolib.fst.bad_uso)
    by_dim = partition(data, get_dimension)
    by_dim = sorted(by_dim.iteritems())

    # by_dim is list of (dimension, dict) tuples.
    # dicts have same format as get_execution_data

    for dim, d in by_dim:
        main(dim, d)

