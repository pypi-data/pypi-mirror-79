#
# this is to run PappaPronta as a package
#

import sys
import os

if __name__ == '__main__':
	ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	sys.path.insert(0, ROOT_PATH)
	sys.path.append('.')
	
	if len(sys.argv) < 2:
	  print("Usage: %s <yaml configuration file>", file=sys.stderr)
	  sys.exit(-1)
	
	from PappaPronta.creator.creator import Creator
	
	yaml_file = sys.argv[1]
	
	c = Creator(yaml_file)
	print(c.output())
	
	sys.exit(0)
