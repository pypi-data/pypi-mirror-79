import os

def root_path():
    """root_path

       root_path() returns the root path of the PappaPronta library
    """

    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
