from PappaPronta.patterns.pattern import Pattern

class Function(Pattern):
    """The Function class
    
    The Function class returns a value for any allowed time
    it gets as argument. It has all the methods from its parent class, Pattern
    plus a vector of factor values (empty by default)
    """

    def __init__(self, at, dur, factors = []):
        super(Function, self).__init__(at, dur)
        self.setup(factors)

    def setup(self, factors):
        pass

    def next(self, t):
        super(Function, self).next(t)
        return None

    def __eq__(self, other):
        res = False
        res = super(Function, self).__eq__(other)
        if not res or not isinstance(other, Function):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return res

    @classmethod
    def create(cls, at, dur, dict = {}):
        dvalues = eval(dict['factors'])
        return cls(at, dur, dvalues)
