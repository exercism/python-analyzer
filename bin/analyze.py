#! /usr/bin/env python3
"""
CLI for the auto-analyzer for the Python track on Exercism.io.
"""
import argparse
import importlib.util
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve(strict=True)
LIBRARY = ROOT.parent.parent.joinpath("lib").resolve(strict=True)
ANALYZERS = {f.parent.name: f for f in LIBRARY.glob("*/analyzer.py")}

class Exercise(NamedTuple):
    """
    An individual Exercise to anaylze.
    """

    name: str
    path: Path
    tests_path: Path

    def analyze(self):
        """
        Perform automatic analysis on this Exercise.
        """
        module_name = f"{self.path.name}_analyzer"
        module = ANALYZERS[self.name]
        spec = importlib.util.spec_from_file_location(module_name, module)
        analyzer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(analyzer)
        sys.modules[module_name] = analyzer
        return analyzer.analyze(str(self.path))

    @staticmethod
    def sanitize_name(name: str) -> str:
        """
        Sanitize an Exercise name (ie "two-fer" -> "two_fer").
        """
        return name.replace("-", "_")

    @classmethod
    def factory(cls, name: str, directory: Path) -> "Exercise":
        """
        Build an Exercise from its name and the directory where its files exist.
        """
        sanitized = cls.sanitize_name(name)
        path = directory.joinpath(f"{sanitized}.py").resolve()
        tests_path = directory.joinpath(f"{sanitized}_test.py").resolve()
        return cls(name, path, tests_path)


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
        choices=ANALYZERS.keys(),
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
