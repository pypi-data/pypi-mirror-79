from PappaPronta.events.event import Event

class CsoundEvent(Event):
    """The CsoundEvent class
    
    The CsoundEvent class is the class that handles csound writing.
    It has the basic properties of events and differs only in the
    output() method.
    """

    def __init__(self, at, dur, instr, parms, msg = ''):
        super(CsoundEvent, self).__init__(at, dur, parms)
        self.instrument = instr
        self.message = msg

    def output(self):
        result = "i%03d %8.4f %8.4f " % (self.instrument, self.at, self.dur)
        for k in self.parameters:
            result += ("%8.4f " % (k))
        result += self.message
        return result
