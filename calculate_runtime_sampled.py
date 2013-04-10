import itertools, random, multiprocessing, time

import usolib


def main(n):
    res = usolib.randomfacet.randomfacet_sample(usolib.fst.bad_uso, n)
    return res


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=8)
    
    print " n\ttime\tavg runtime"
    for n in range(1, 51):
        t = time.time()
        N = 10000
        async_result = pool.map_async(main, [n for i in range(N)])
        while not async_result.ready():
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                pool.terminate()
                pool.join()
                exit()
        lst = async_result.get()
        res = sum(lst) / float(N)
        print "%2d\t%4.2fs\t%.4f" %(n, time.time() - t, res)

