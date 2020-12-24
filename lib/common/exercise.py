"""
Helpers for exercise discovery and execution.
"""
import sys
import importlib
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve(strict=True).parent
LIBRARY = ROOT.parent.resolve(strict=True)

# map each available exercise name to its EXERCISE/anaylzer.py module
ANALYZERS = {f.parent.name: f for f in LIBRARY.glob("*/analyzer.py")}


class ExerciseError(Exception):
    """
    Exception to raise if there's a problem building an Exercise
    """


class Exercise(NamedTuple):
    """
    Manages analysis of a an individual Exercise.
    """

    name: str
    in_path: Path
    out_path: Path
    tests_path: Path

    @property
    def analyzer(self):
        """
        The analyzer.py module for this Exercise, imported lazily.
        """
        module_name = f"{Exercise.sanitize_name(self.name)}_analyzer"
        if module_name not in sys.modules:
            module = self.available_analyzers()[self.name]
            spec = importlib.util.spec_from_file_location(module_name, module)
            analyzer = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(analyzer)
            sys.modules[module_name] = analyzer
        return sys.modules[module_name]

    @property
    def comments(self):
        """
        The comments defined in the analyzer.py module.
        """
        return self.analyzer.Comments

    def analyze(self):
        """
        Perform automatic analysis on this Exercise.
        """
        return self.analyzer.analyze(self.in_path, self.out_path)

    @staticmethod
    def sanitize_name(name: str) -> str:
        """
        Sanitize an Exercise name (ie "two-fer" -> "two_fer").
        """
        return name.replace("-", "_")

    @classmethod
    def available_analyzers(cls):
        """
        Returns the map of avaiable EXERCISE/analyzer.py files.
        """
        return ANALYZERS

    @classmethod
    def factory(cls, name: str, in_directory: Path, out_directory: Path) -> "Exercise":
        """
        Build an Exercise from its name and the directory where its files exist.
        """
        if name not in cls.available_analyzers():
            path = LIBRARY.joinpath(name, "analyzer.py")
            raise ExerciseError(f"No analyzer discovered at {path}")
        sanitized = cls.sanitize_name(name)
        in_path = in_directory.joinpath(f"{sanitized}.py").resolve()
        out_path = out_directory.joinpath(f"{sanitized}.py").resolve()
        tests_path = in_directory.joinpath(f"{sanitized}_test.py").resolve()
        return cls(name, in_path, out_path, tests_path)
