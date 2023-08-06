from PappaPronta.patterns.sequence import Sequence

class AutoSequence(Sequence):
    """The AutoSequence class
    
    The AutoSequence class behaves like a Sequence, except
    the values are created automatically by the fill() method which is called
    at startup time.
    """

    def __init__(self, at, dur):
        self.values = []
        super(AutoSequence, self).__init__(at, dur)

    def setup(self):
        self.index = 0
        self.fill()
        self.size = len(self.values)

    def fill(self):
        pass         # this is supposed to be filled up in derived classes
