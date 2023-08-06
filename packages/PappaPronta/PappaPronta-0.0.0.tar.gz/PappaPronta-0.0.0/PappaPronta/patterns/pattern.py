from PappaPronta.core.base import Base

class Pattern(Base):
    """The Pattern class
    
    The Pattern class is the base class for all sequencing objects.
    It has only basic instance methods:
        * next(t): gets the next event at time t
    It has a class method:
        * create(at, dur, dict): allows to create the class from a dictionary
    """

    def __init__(self, at, dur):
        super(Pattern, self).__init__(at, dur)

    def next(self, t):
        if not self.check_time(t):
            raise ValueError(t)
        return t

    #
    # we need this to make assertions work in unit tests (grrrrrr)
    #
    def __eq__(self, other):
        if not isinstance(other, Pattern):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.at == other.at and self.dur == other.dur

    #
    # create is supposed to be modified in inherited classes
    #
    @classmethod
    def create(cls, at, dur, dict = {}):
        return cls(at, dur)
