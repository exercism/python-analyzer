#! /usr/bin/env python3
"""
CLI for the auto-analyzer for the Python track on Exercism.io.
"""
import argparse
import importlib.util
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve(strict=True).parent
LIBRARY = ROOT.parent.joinpath("lib").resolve(strict=True)

# add the library to sys.path so common modules can be imported by analyzer
if str(LIBRARY) not in sys.path:
    sys.path.insert(0, str(LIBRARY))

from common import Exercise, ExerciseError


def main():
    """
    Parse CLI arguments and perform the analysis.
    """

    def directory(path: str) -> Path:
        selection = Path(path)
        if not selection.is_dir():
            raise argparse.ArgumentTypeError(f"{selection} must be a directory")
        return selection

    parser = argparse.ArgumentParser(
        description="Perform automatic code analysis of a Python track exercise."
    )
    parser.add_argument(
        "exercise",
        metavar="EXERCISE",
        type=str,
        choices=sorted(Exercise.available_analyzers().keys()),
        help="name of the exercise to analyze (One of: %(choices)s)",
    )
    parser.add_argument(
        "directory",
        metavar="DIR",
        type=directory,
        help="directory where the the [EXERCISE].py file located",
    )
    args = parser.parse_args()

    exercise = Exercise.factory(args.exercise, args.directory)
    exercise.analyze()


if __name__ == "__main__":
    main()
