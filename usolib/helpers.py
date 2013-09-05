import time, multiprocessing, operator, os, sys, signal, functools, random

from collections import Counter


def memoize(cache=None, cache_key=lambda *x: x):
    if cache is None:
        cache = {}
    def decorator(f):
        def inner(*args):
            k = cache_key(*args)
            if k in cache:
                return cache[k]
            res = f(*args)
            cache[k] = res
            return res
        return inner
    return decorator


def factorial(n):
    return reduce(operator.mul, xrange(1, n+1), 1.0)


def nck(n,k):
    return factorial(n) / (factorial(k) * factorial(n-k))


def average(itr):
    """
    Average implementation that handles iterators well and doesn't consume extra memory, 
    in exchange for a slower speed.
    """
    total = 0
    count = 0
    for i in itr:
        total += i
        count += 1
    return total / float(count)


def matousek_runtime(k):
    """
    Expected runtime of randomly chosen matousek uso
    """
    return sum(0.5**l / factorial(l) * nck(k, l)
               for l in range(1, k+1))


def int_to_vertex(x, n):
    return bin(x)[2:].zfill(n)


def generate_vertices(n, start=0, step=1):
    return (int_to_vertex(i, n) for i in xrange(start, 2**n, step))


def get_dimension(cube):
    return cube.count("*")


def global2local(vertex, subcube):
    if vertex is None:
        return None
    return "".join(val for (val, dim) in zip(vertex, subcube) if dim == "*")

def local2global(vertex, subcube):
    if vertex is None:
        return None
    itr = iter(vertex)
    return "".join(dim if dim != "*" else next(itr) for dim in subcube)


class CountingDict(dict):
    def __init__(self):
        self.counter = Counter()

    def __contains__(self, val):
        self.counter[val] += 1
        return False


pool = None

def pmap(f, data, processes=1, args=(), batchsize=1000):
    """
    Paralell map.
    """
    # functools.partial is safe as it can be pickled, unlike lambdas
    f = functools.partial(f, *args)

    if processes == 1:
        return map(f, data)

    old_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

    # initialize pool the first time pmap is called
    global pool
    if pool is None:
        pool = multiprocessing.Pool(processes=processes)
    elif processes != pool._processes:
        print ("Warning: %d processes requested, but pool already initialized with %d." 
               % (processes, pool._processes))

    def handler(*a):
        pool.terminate()
        sys.stdout.write(" Interrupted!\n")
        sys.stdout.flush()
        pool.join()
        sys.exit(1)

    signal.signal(signal.SIGINT, handler)

    # split data into chunks to feed the workers as soon as possible.
    # TODO: can single jobs be submitted to pool?
    data_itr = iter(data)
    batch = [i for (i, _) in zip(data_itr, range(batchsize*processes))]
    async_results = []

    while batch:
        async_results.append(pool.map_async(f, batch))
        batch = [i for (i, _) in zip(data_itr, range(batchsize*processes))]

    signal.signal(signal.SIGINT, old_handler)

    # wait for all batches to finish
    for result in async_results:
        while not result.ready():
            time.sleep(0.01)

    # compile and return results
    res = []
    for result in async_results:
        res.extend(result.get())
    return res


