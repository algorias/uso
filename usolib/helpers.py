import time, multiprocessing, operator

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



def pmap(f, data, processes=None):
    """
    Paralell map.
    """
    if processes == 1:
        return map(f, data)

    # TODO: catch keyboardinterrupts cleanly
    pool = multiprocessing.Pool(processes=processes)

    async_result = pool.map_async(f, data)
    try:
        while not async_result.ready():
            time.sleep(0.01)
    except KeyboardInterrupt:
        pool.terminate()
        pool.join()
        exit()
    
    return async_result.get()


