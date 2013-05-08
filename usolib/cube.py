

class Cube(object):
    """
    Cube.

    Instances of this are immutable, which makes working with them easier and safer.
    """

    def _tuple_to_string(self, data):
        d = {"0": 0,
             "1": 1,
             "*": 9}
        return "".join(d[i] for i in data)


    def _string_to_tuple(self, data):
        d = {0: "0",
             1: "1",
             9: "*"}
        return tuple(d[char] for char in data)
        

    def __init__(self, data):
        if isinstance(data, basestring):
            # convert from string
            self.data = self._string_to_tuple(data)
        else:
            # assume data is some iterable.
            self.data = tuple(i for i in data)


    def to_string(self):
        return self._tuple_to_string(self.data)


    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.to_string())


    def flip(self, i):
        assert self[i] != 9
        return Cube(self[:i] + [not self[i]] + self[i+1:])


    def split(self, dim, facet):
        """ 
        Return one of the facets when splitting along dimension dim.
        """
        assert self[dim] == 9
        return Cube(self[:dim] + [facet] + self[dim+1:])


    @property
    def dim(self):
        return self.data.count(9)


    def __getitem__(self, i):
        return self.data[i]


    def __hash__(self):
        #return hash(self.get_str())
        return hash(self.data)



class Vertex(Cube):
    """
    Special case of a cube. 
    
    This class is not strictly needed, but makes code more readable.
    """
    _char_to_int = int
    _int_to_char = str

    @property
    def dim(self):
        return 0

    def split(self, *args):
        raise TypeError("Can't split a vertex")

