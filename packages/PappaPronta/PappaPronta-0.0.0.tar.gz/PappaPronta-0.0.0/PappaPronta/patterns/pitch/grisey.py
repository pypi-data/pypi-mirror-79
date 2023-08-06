from PappaPronta.patterns.auto_sequence import AutoSequence
from PappaPronta.patterns.pitch.sieve import sieve

class Grisey(AutoSequence):
    """The Grisey class
    
    The Grisey class behaves like a Sequence, except
    the values are created automatically by the fill() method which is called
    at startup time. In particular, this class implement the prime number
    harmonic technique developed by French composer Gerard Grisey. This
    technique consists in selecting pitches from higher range prime number harmonics of a
    very very low frequency (sub-audio)

    The properties of this object are:
        * base_frequency: the fundamental frequency
        * start_prime: the first prime number to be used in the series
        * end_prime: the last prime number to be used in the series
    """

    def __init__(self, at, dur, base_freq, start_p, end_p):
        self.base_frequency = base_freq
        self.start_prime = start_p
        self.end_prime = end_p
        super(Grisey, self).__init__(at, dur)


    def fill(self):
        l = sieve(self.start_prime, self.end_prime)
        self.values = [float(self.base_frequency)*p for p in l]

