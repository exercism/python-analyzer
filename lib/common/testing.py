"""
Helpers for unit testing an exercise's analyzer.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
from .exercise import Exercise
from .analysis import Status


class BaseExerciseTest(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """
        The name of the exercise under test (ie `two-fer`)
        """
        ...

    @classmethod
    def setUpClass(cls):
        """
        Creates the temporary working area for files.
        """
        cls.root = TemporaryDirectory()

    @classmethod
    def tearDownClass(cls):
        """
        Cleans up the temporary working area for files.
        """
        cls.root.cleanup()

    def setUp(self):
        """
        Basic test setup.
        """
        self.exercise = Exercise.factory(
            self.name, Path(self.root.name).resolve(strict=True)
        )
        self.analyzer = self.exercise.analyzer
        self.comments = self.exercise.comments

    def write_test_file(self, content: str):
        """
        Write the given content to the test file in the working area.
        """
        self.exercise.path.write_text(content.strip())

    def clean_test_file(self):
        """
        Clean up the test file.
        """
        if self.exercise.path.exists():
            self.exercise.path.unlink()

    def get_analysis(self, content: Optional[str]):
        """
        Write the given content to the test file and return the analysis of it.
        If content is None, clear the test file.
        """
        if content is None:
            self.clean_test_file()
        else:
            self.write_test_file(content)
        return self.exercise.analyze()

    def tearDown(self):
        """
        Basic test cleanup.
        """
        self.clean_test_file()

    def test_no_module(self):
        """
        Ensure the analyzer can handle a missing module.
        """
        analysis = self.get_analysis(None)
        self.assertIs(analysis.status, Status.DISAPPROVE_WITH_COMMENT)
        self.assertIn(self.comments.NO_MODULE, analysis.comment)
        self.assertIs(analysis.approved, False)

    def test_has_module(self):
        """
        Ensure the analyzer does not label an existing module as missing.
        """
        analysis = self.get_analysis("pass")
        self.assertNotIn(self.comments.NO_MODULE, analysis.comment)

    def test_has_malformed_code(self):
        """
        Ensure the analyzer can handle malformed code.
        """
        analysis = self.get_analysis("fed test();")
        self.assertIs(analysis.status, Status.DISAPPROVE_WITH_COMMENT)
        self.assertIn(self.comments.MALFORMED_CODE, analysis.comment)
        self.assertIs(analysis.approved, False)

    def test_no_malformed_code(self):
        """
        Ensure the analyzer does not mark working code as malformed.
        """
        analysis = self.get_analysis("pass")
        self.assertNotIn(self.comments.MALFORMED_CODE, analysis.comment)
