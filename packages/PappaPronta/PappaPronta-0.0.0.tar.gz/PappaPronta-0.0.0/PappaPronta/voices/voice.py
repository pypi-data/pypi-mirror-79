from PappaPronta.core.base import Base
from PappaPronta.patterns.all_patterns import *

class Voice(Base):
    """The Voice class
    
    The Voice class is the base class for all voicing objects.
    It has only basic properties:
        * parameters: a list of parameters (which may either be empty or a
                list of subclasses of Pattern objects); these parameters are
                supposed to be used in the generate() method to build the list
                of output objects (defalt: empty)
        * fields: a dictionary of fields (which may be either empty or a
                dictionary of subclasses of the Pattern object); these parameters are
                supposed to be used in the generate() method to build the
                parameters of each output event (defalt: empty)
    It's methods are:
        * output(): a method which calls all the outputs of the events
                    collected
        * generate(): a method that gets called at creation to generate all
                      events of a given voice
    A class method (create()) allows to create it from a yaml dictionary
    """

    def __init__(self, at, dur, cls, pars = {}, flds = []):
        self.at = at
        self.dur = dur
        self.classname = cls
        self.parameters = pars
        self.fields = flds
        self.events = []
        self.check_parameters()
        self.generate()

    def check_parameters(self):
        for v in self.parameters.values():
            if not isinstance(v, Pattern):
                raise TypeError('Parameter values must all be Pattern-like objects')
        for f in self.fields:
            if not isinstance(f, Pattern):
                raise TypeError('Fields must all be Pattern-like objects')

    def output(self):
        result = []
        for e in self.events:
            result.append(e.output())
        result.append('') # To add a final return
        return '\n'.join(result)

    def generate(self):
        pass

    @classmethod
    def create(cls, dict):
        return cls.parse_dictionary(dict)

    @classmethod
    def parse_dictionary(cls, dict):
        at = dict['at']
        dur = dict['dur']
        pars = {}
        flds = []
        for k, v in dict['parameters'].items():
            val = Voice.parse_value(v, at, dur)
            pars[k] = val
        flds = [Voice.parse_value(v, at, dur) for v in dict['fields']]
        return cls(at, dur, dict['class'], pars, flds)

    @classmethod
    def parse_value(cls, v, at, dur):
        (kname, sargs) = v.split('(', 1)
        sargs = sargs.replace(')', '')
        klass = eval(kname)
        vargs  = eval(sargs)
        return klass(at, dur, vargs)
