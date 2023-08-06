from PappaPronta.patterns.function import Function

class Linear(Function):
    """The Linear class
    
    The Linear class returns a linear interpolation value for any allowed time
    it gets as argument. It has all the methods from its parent class, Pattern.
    """

    def __init__(self, at, dur, factors):
        super(Linear, self).__init__(at, dur, factors)
        self.setup(factors)

    def setup(self, factors):
        self.start_value = float(factors[0])
        self.end_value = float(factors[1])
        self.a_factor = (self.end_value - self.start_value) / float(self.dur)
        self.b_factor = self.start_value - (self.a_factor * self.at)

    def next(self, t):
        super(Linear, self).next(t)
        return (self.a_factor*t) + self.b_factor

    def __eq__(self, other):
        res = False
        res = super(Linear, self).__eq__(other)
        if not res or not isinstance(other, Linear):
            # don't attempt to compare against unrelated types
            return NotImplemented
        res = (self.start_value == other.start_value) and (self.end_value == other.end_value) and (self.a_factor == other.a_factor) and (self.b_factor == other.b_factor)
        return res
