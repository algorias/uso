import itertools

from usolib.helpers import memoize

class SimpleFST(object):
    """
    An implementation of a simple finite state transducer.

    Inputs are words in {0,1}*
    Outputs are words in {+,-}*
    Subcubes are words in {0,1,*}*, where * means that dimension is spanned by the subcube.

    transition table is a dict that maps (state, input) to (state, output)

    Interpreting the input as a vertex of a hypercube, the output gives the orientation of the incident
    edges, where + means incoming. This induces a USO on any hypercube, as long as each state outputs + for one
    input and - for the other.
    """

    def __init__(self, table=None, start=0, edges=None):
        # two ways to initialize the automaton, keep both for compatibility
        if table is None:
            assert edges is not None
            table = self.table_from_edges(edges)
        else:
            assert edges is None
        self.table = table
        self.states = set(state for (state, v) in self.table)
        self.start_state = start
        self.k = len(self.states)
        self.validate_table()
        self.build_inverse_table()


    def validate_table(self):
        """ Check if table describes a simple FST."""
        assert self.start_state in self.states

        for state in self.states:
            # make sure transitions exist and are valid
            nextstate, out0 = self.table[state, "0"]
            assert nextstate in self.states
            assert out0 in "+-"

            nextstate, out1 = self.table[state, "1"]
            assert nextstate in self.states
            assert out1 in "+-"

            # make sure state is either even or odd
            assert out0 != out1

    
    def build_inverse_table(self):
        """ Precalculate inverse state transition table to find + and - transitions easily."""
        self.inv_table = {}

        for state in self.states:
            nextstate, out = self.table[state, "0"]
            self.inv_table[state, out] = nextstate, "0"
            nextstate, out = self.table[state, "1"]
            self.inv_table[state, out] = nextstate, "1"

   
    def transduce(self, vertex):
        # implements the outmap of the USO generated by the automaton
        state = self.start_state
        for v in vertex:
            state, out = self.table[state, v]
            yield out


    def outmap(self, vertex, subcube):
        # NOTE: subcubes are described by words in {0,1,*}*
        # this method makes no attempt to validate that the vertex actually belongs to the subcube
        return [o for (o, s) in zip(self.transduce(vertex), subcube) if s == "*"]
    

    def find_sink(self, subcube):
        # find sink through structure of automaton, i.e. cheating
        res = []
        state = self.start_state
        for i, dim in enumerate(subcube):
            if dim == "*":
                state, v = self.inv_table[state, "+"]
            else:
                # jump
                state, _ = self.table[state, dim]
                v = dim
            res.append(v)
        return "".join(res)


    def fingerprint(self, n):
        """
        Unroll automaton into tree of depth n, then make a fingerprint out of the DFS of that tree.

        If two such fingerprints are equal, then the automatons are equivalent up to n dimensions.
        """
        return "".join(self._fingerprint_itr(n, self.start_state))


    def _fingerprint_itr(self, n, state):
        if n <= 0:
            return
        nextstate, out = self.table[state, "0"]
        yield out
        for i in self._fingerprint_itr(n-1, nextstate):
            yield i
        nextstate, out = self.table[state, "1"]     
        for i in self._fingerprint_itr(n-1, nextstate):
            yield i


    @memoize()
    def fingerprint_subcube(self, subcube):
        """
        produce a fingerprint of the transducer of a subcube.
        doesn't guarantee absolutely identical automatons, only identical up to the dimension they're being
        evaluated to.
        """
        return "".join(self._fingerprint_subcube_itr(subcube, self.start_state))


    def _fingerprint_subcube_itr(self, subcube, state):
        if subcube == "":
            return

        head = subcube[0]
        subcube = subcube[1:]
        if head == "*":
            nextstate, out = self.table[state, "0"]
            yield out
            for i in self._fingerprint_subcube_itr(subcube, nextstate):
                yield i
            nextstate, out = self.table[state, "1"]     
            for i in self._fingerprint_subcube_itr(subcube, nextstate):
                yield i
        else:
            nextstate, _ = self.table[state, head]
            for i in self._fingerprint_subcube_itr(subcube, nextstate):
                yield i
        

    def get_edges(self):
        edges = [(q_old, a, b, q_new) for ((q_old, a), (q_new, b)) in self.table.iteritems()]
        return sorted(edges)


    def table_from_edges(self, edges):
        return dict(((q_old, a), (q_new,b)) for (q_old, a, b, q_new) in edges)


def uniq(usos, n):
    """
    Take an iterator of usos and remove functional duplicates up to dimension n.
    """
    d = dict((uso.fingerprint(n), uso) for uso in usos)
    return d.values()

