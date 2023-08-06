from PappaPronta.core.base import Base

class Event(Base):
    """The Event class
    
    The Event class is the base class for all Event (output) objects.
    It has only basic properties:
        * parameters: an array of other, user-defined, parameters
    It has only basic methods:
        * output: an output method for all Events (to be rewritten for each
                specific type of event
    """

    def __init__(self, at, dur, parms):
        super(Event, self).__init__(at, dur)
        self.parameters = parms

    def output(self):
        return "Event: action time %8.4f, dur %8.4f" % (self.at, self.dur)
