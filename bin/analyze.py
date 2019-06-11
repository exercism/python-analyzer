import sys
import os


file_path = os.path.join(sys.argv[2], ' {}.py'.format(sys.argv[1].replace('-', '_')))

# Add path to import analyzer
sys.path.append('../lib/{}'.format(sys.argv[1]))

import analyzer
analyzer.analyze(file_path)