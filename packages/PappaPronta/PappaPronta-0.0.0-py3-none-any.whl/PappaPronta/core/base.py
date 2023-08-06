class Base(object):
    """The base class
    
    The Base class is the base class for all PappaPronta objects.
    It has only basic properties:
        * action time: start of validity
        * duration: the duration of validity
    It has only basic methods:
        * end(): gets the end time for events
        * check_time(t): checks whether t falls between at and endt
    """

    def __init__(self, at, dur):
        self.at = at
        self.dur = dur

    def end(self):
        return self.at + self.dur

    def check_time(self, t):
        return True if (t >= self.at and t <= self.end()) else False
