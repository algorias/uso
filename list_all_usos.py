
import usolib
from usolib.helpers import *
from usolib.graph_helpers import *


if __name__ == "__main__":
    K = 4
    usos_itr = usolib.uso.all_by_states(K)
    fd = open("/home/vitor/usos.txt", "w")
    test_set = set([""])
    count = 0
    raw_count = 0

    for uso in usos_itr:
        raw_count += 1
        if not raw_count % 1000:
            print "%8d  %8d" % (raw_count, count)

        #fingerprint = uso.fingerprint(2*K - 1)
        fingerprint = hopcroft_fingerprint(uso)
        if fingerprint in test_set:
            continue
        test_set.add(fingerprint)
        print >> fd, ", ".join(str(i) for i in uso.get_edges())
        count += 1

    print "%7d  %7d" % (raw_count, count)
    
