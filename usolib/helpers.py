import time, multiprocessing, operator, os, sys, signal, functools

from collections import Counter


def memoize(cache=None):
    if cache is None:
        cache = {}
    def decorator(f):
        def inner(*args):
            if args not in cache:
                cache[args] = f(*args)
            return cache[args]
        return inner
    return decorator


def factorial(n):
    return reduce(operator.mul, xrange(1, n+1), 1.0)


def int_to_vertex(x, n):
    return bin(x)[2:].zfill(n)


def generate_vertices(n, start=0, step=1):
    return (int_to_vertex(i, n) for i in xrange(start, 2**n, step))


def get_dimension(cube):
    return cube.count("*")


class CountingDict(dict):
    def __init__(self):
        self.counter = Counter()

    def __contains__(self, val):
        self.counter[val] += 1
        return False


pool = None

def pmap(f, data, processes=1, args=()):
    """
    Paralell map.
    """
    f = functools.partial(f, *args)

    if processes == 1:
        return map(f, data)

    old_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)

    #pool = multiprocessing.Pool(processes=processes)

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

    async_result = pool.map_async(f, data)
    while not async_result.ready():
        time.sleep(0.01)

    signal.signal(signal.SIGINT, old_handler)

    return async_result.get()


