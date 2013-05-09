import fst

# trivial uso with 1...1 as the sink
table = {(0, "0"): (0, "-"),
         (0, "1"): (0, "+")}
ascending = fst.SimpleFST(table)


# slow uso that is not matousek
table = {(0, "0"): (1, "+"),
         (0, "1"): (2, "-"),
         (1, "0"): (2, "-"),
         (1, "1"): (0, "+"),
         (2, "0"): (0, "+"),
         (2, "1"): (1, "-")}
bad = fst.SimpleFST(table)


# slow uso that is matousek, with a matrix of the form:
#    1
#    1 1
#    0 1 1
#    1 0 1 1
#    1 1 0 1 1
#    0 1 1 0 1 1
table = {("start", "0"): ("start", "+"),
         ("start", "1"): ("e2", "-"),
         ("e1", "0"): ("e2", "-"),
         ("e1", "1"): ("start", "+"),
         ("e2", "0"): ("o1", "-"),
         ("e2", "1"): ("e1", "+"),
         ("o1", "0"): ("e1", "+"),
         ("o1", "1"): ("o1", "-")}
test = fst.SimpleFST(table, start_state="start")

del table

