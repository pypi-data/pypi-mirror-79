from root_path import root_path
import sys

def setup_path():
    """setup_path

       setup_path sets the path of the PappaPronta library accordingly so that
       it can import files in a decent way
    """

    sys.path.append(root_path())
