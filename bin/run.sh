#!/bin/sh

# Usage:
# ./bin/run.sh two_fer ~/test/
export PYTHONPATH=/opt/analyzer/lib/$1/
python bin/run.py $1 $2
