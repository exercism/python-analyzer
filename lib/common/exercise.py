"""
Helpers for exercise discovery and execution.
"""
import sys
import importlib
import json
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

    slug: str
    in_path: Path
    out_path: Path
    tests_path: Path

    @property
    def analyzer(self):
        """
        The analyzer.py module for this Exercise, imported lazily.
        """
        module_name = f"{Exercise.sanitize_name(self.slug)}_analyzer"

        if module_name not in sys.modules:
            module = self.available_analyzers()[self.slug]
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
    def sanitize_name(slug: str) -> str:
        """
        Sanitize an Exercise name (ie "two-fer" -> "two_fer").
        """
        return slug.replace("-", "_")

    @classmethod
    def available_analyzers(cls):
        """
        Returns the map of available EXERCISE/analyzer.py files.
        """
        return ANALYZERS

    @classmethod
    def factory(cls, slug: str, in_directory: Path, out_directory: Path) -> "Exercise":
        """
        Build an Exercise from its name and the directory where its files exist.
        """

        if slug not in cls.available_analyzers():
            path = LIBRARY.joinpath(slug, "analyzer.py")
            raise ExerciseError(f"No analyzer discovered at {path}")

        in_path = None
        out_path = None
        tests_path = None

        config_file = in_directory.joinpath(".meta").joinpath("config.json")

        if config_file.is_file():
            config_data = json.loads(config_file.read_text())
            in_path = in_directory.joinpath(config_data.get('files', {}).get('solution')[0])
            out_path = out_directory.joinpath(config_data.get('files', {}).get('solution')[0])
            tests_path = in_directory.joinpath(config_data.get('files', {}).get('test')[0])

        else:
            sanitized = cls.sanitize_name(slug)
            in_path = in_directory.joinpath(f"{sanitized}.py").resolve()
            out_path = out_directory.joinpath(f"{sanitized}.py").resolve()
            tests_path = in_directory.joinpath(f"{sanitized}_test.py").resolve()

        return cls(slug, in_path, out_path, tests_path)
