import importlib
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from PappaPronta.voices.voice import *

class Creator:
    """The Creator class
    
    The Creator class is the class that create all voice objects starting
    from a Yaml file description.
    It takes a yaml file name as argument
    """

    def __init__(self, yaml_filename):
        with open(yaml_filename, 'r') as yaml_file:
            self.yaml_config = load(yaml_file, Loader=Loader)
        self.voices = []
        self.parse_configuration()

    def parse_configuration(self):
        for v in self.voice_keys():
            self.parse_voice(self.yaml_config[v])

    def parse_voice(self, voice):
        mod = voice['class'].casefold()
        klass = self.dynamic_importer(mod, voice['class'])
        self.voices.append(klass.create(voice))

    def generate(self):
        for v in self.voices:
            v.generate()

    def output(self):
        result = [self.header()]
        for v in self.voices:
            result.append(v.output())
        result.append(self.trailer())
        return ''.join(result)

    def dynamic_importer(self, modname, classname):
        mod = __import__(modname, fromlist=[classname])
        return getattr(mod, classname)

    def header(self):
        return ''.join([self.yaml_config['decorators']['header'], '\n'])

    def trailer(self):
        return ''.join([self.yaml_config['decorators']['trailer'], '\n'])

    def voice_keys(self):
        result = []
        for key in self.yaml_config.keys():
            if "voice" in key.lower():
                result.append(key)
        return result
