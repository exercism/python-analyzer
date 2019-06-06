#!/bin/sh

# Usage:
# ./bin/analyze.sh two_fer ~/test/
export PYTHONPATH=/opt/analyzer/lib/$1/
python bin/analyze.py $1 $2
