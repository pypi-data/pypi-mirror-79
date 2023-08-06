#
# this module loads everything that is needed in tests
#

import pdb
import sys
import os
import unittest

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_PATH)
import PappaPronta
