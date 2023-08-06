from PappaPronta.patterns.pattern import Pattern

class Constant(Pattern):
    """The Constant class
    
    The Constant class returns the same value for any allowed time it gets
    in the input. It has all the methods from its parent class, Pattern.
    """

    def __init__(self, at, dur, value):
        super(Constant, self).__init__(at, dur)
        self.value = value

    def next(self, t):
        super(Constant, self).next(t)
        return self.value

    def __eq__(self, other):
        res = False
        res = super(Constant, self).__eq__(other)
        if not res or not isinstance(other, Constant):
            # don't attempt to compare against unrelated types
            return NotImplemented
        res = self.value == other.value
        return res

    @classmethod
    def create(cls, at, dur, value):
        return cls(at, dur, float(value))
