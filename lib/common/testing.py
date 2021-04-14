"""
Helpers for unit testing an exercise's analyzer.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional
from .analysis import Analysis
from .comment import BaseFeedback, Summary
from .exercise import Exercise, ExerciseError

BAD_CODE = "fed test();"

class BaseExerciseTest(ABC):
    @property
    @abstractmethod
    def slug(self) -> str:
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
        self.exercise = Exercise.factory(self.slug,
                                         Path(self.root.name).resolve(strict=True),
                                         Path(self.root.name).resolve(strict=True))
        self.analyzer = self.exercise.analyzer
        self.comments = self.exercise.comments

    def write_test_file(self, content: str):
        """
        Write the given content to the test file in the working area.
        """

        #add newline to content to keep pylint happy
        clean_content = f"{content.strip()}\n"

        self.exercise.out_path.write_text(clean_content)

    def clean_test_file(self):
        """
        Clean up the test file.c
        """
        if self.exercise.out_path.exists():
            self.exercise.out_path.unlink()

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
        self.assertIs(analysis.summary, Summary.REQUIRE)
        self.assertIn(self.comments.MALFORMED_CODE,  [item.comment for item in analysis['comments']])

    def test_has_module(self):
        """
        Ensure the analyzer does not label an existing module as missing.
        """
        analysis = self.get_analysis("pass")
        self.assertNotIn(self.comments.NO_MODULE,  [item.comment for item in analysis['comments']])

    def test_has_malformed_code(self):
        """
        Ensure the analyzer can handle malformed code.
        """
        analysis = self.get_analysis(BAD_CODE)
        print(analysis)
        self.assertIs(analysis.summary, Summary.REQUIRE)
        self.assertIn(self.comments.MALFORMED_CODE,  [item.comment for item in analysis['comments']])

    def test_no_malformed_code(self):
        """
        Ensure the analyzer does not mark working code as malformed.
        """
        analysis = self.get_analysis("pass")
        self.assertNotIn(self.comments.MALFORMED_CODE,  [item.comment for item in analysis['comments']])
