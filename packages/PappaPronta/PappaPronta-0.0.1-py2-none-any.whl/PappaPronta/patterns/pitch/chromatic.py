from PappaPronta.patterns.auto_sequence import AutoSequence

class Chromatic(AutoSequence):
    """The Chromatic class
    
    The Chromatic class behaves like a Sequence, except
    the values are created automatically by the fill() method which is called
    at startup time.

    The properties of this object are:
        * start_frequency: the lowest frequency
        * number_of_notes: the number of notes of the whole set
        * octave_base: the octave multiplication factor (default: 2)
        * notes_per_octave: the number of notes per octave (default: 12)
    """

    def __init__(self, at, dur, startfrq, numnotes, octbase = 2, npo = 12):
        self.start_frequency = startfrq
        self.number_of_notes = numnotes
        self.octave_base = octbase
        self.notes_per_octave = npo
        super(Chromatic, self).__init__(at, dur)


    def fill(self):
        self.values = [(float(self.start_frequency)*(float(self.octave_base)**(x/float(self.notes_per_octave)))) for x in range(self.number_of_notes)]
