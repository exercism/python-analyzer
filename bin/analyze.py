import sys
import os

file_path = '{}{}.py'.format(sys.argv[2], sys.argv[1])
print(file_path)
# Add path to import analyzer
sys.path.append(os.path.realpath(__file__).replace('bin/analyze.py', 'lib'))
import analyzer

analyzer.analyze(file_path)