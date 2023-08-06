from math import exp, log
from PappaPronta.patterns.function import Function

class Expon(Function):
    """The Expon class
    
    The Expon class returns an exponential interpolation value for any allowed time
    it gets as argument. It has all the methods from its parent class, Function.
    """

    def __init__(self, at, dur, factors):
        super(Expon, self).__init__(at, dur, factors)
        self.setup(factors)

    def setup(self, factors):
        self.start_value = float(factors[0])
        self.end_value = float(factors[1])
        self.a_factor = (log(self.end_value) - log(self.start_value)) / float(self.dur)
        self.b_factor = log(self.start_value) - (self.a_factor * self.at)

    def next(self, t):
        super(Expon, self).next(t)
        return exp((self.a_factor*t) + self.b_factor)

    def __eq__(self, other):
        res = False
        res = super(Expon, self).__eq__(other)
        if not res or not isinstance(other, Expon):
            # don't attempt to compare against unrelated types
            return NotImplemented
        res = (self.start_value == other.start_value) and (self.end_value == other.end_value) and (self.a_factor == other.a_factor) and (self.b_factor == other.b_factor)
        return res

    @classmethod
    def create(cls, at, dur, values):
        sv = float(values[0])
        ev = float(values[1])
        return cls(at, dur, sv, ev)
