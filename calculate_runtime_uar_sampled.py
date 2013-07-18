import time

import usolib
from usolib.helpers import *

N = 3

def main(n_samples):
    """
    Generate a random instance and sample its expected runtime.
    """
    uso = usolib.uso.uar(N)
    lst = [usolib.randomfacet.randomfacet_sample(uso, N) for i in range(n_samples)]
    return sum(lst) / float(n_samples)


if __name__ == "__main__":
    n_usos = 1200 # number of random instances generated
    n_samples = 500 # number of times to sample each uso
    lst = pmap(main, [n_samples for i in range(n_usos)], processes=6)
    print "%.4f" % (sum(lst) / float(n_usos))

