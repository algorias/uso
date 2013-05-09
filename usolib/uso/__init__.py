import fst

table = {(0, "0"): (1, "+"),
         (0, "1"): (2, "-"),
         (1, "0"): (2, "-"),
         (1, "1"): (0, "+"),
         (2, "0"): (0, "+"),
         (2, "1"): (1, "-")}
bad = fst.SimpleFST(table)

table = {(0, "0"): (0, "-"),
         (0, "1"): (0, "+")}
ascending = fst.SimpleFST(table)

del table

