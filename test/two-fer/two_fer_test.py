"""
Unit tests for the two-fer analyzer.
"""
import sys
import unittest
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve(strict=True).parent
TESTS = ROOT.parent
REPO = TESTS.parent
LIBRARY = REPO.joinpath("lib").resolve(strict=True)

# add the library to sys.path so common modules can be imported by analyzer
if str(LIBRARY) not in sys.path:
    sys.path.insert(0, str(LIBRARY))

from common import Exercise, Status, BaseExerciseTest

USES_STRING_FORMAT = """
def two_fer(name="you"):
    return "One for {}, one for me.".format(name)
"""

USES_F_STRING = """
def two_fer(name="you"):
    return f"One for {name}, one for me."
"""

USES_PERCENT = """
def two_fer(name="you"):
    return "One for %s, one for me." % name
"""

USES_CONCAT = """
def two_fer(name="you"):
    return "One for " + name + ", one for me."
"""

USES_CONDITIONAL = """
def two_fer(name=None):
    if not name:
        return "One for you, one for me."
    else: 
        return "One for %s, one for me." %name
"""

NO_DEF_ARG = """
def two_fer(name):
    return "One for %s, one for me." % name
"""

NO_RETURN = """
def two_fer(name="you"):
    print ("One for %s, one for me." % name)
"""

WRONG_DEF_ARG = """
def two_fer(name="them"):
    return "One for %s, one for me." % name
"""


class TwoFerTest(BaseExerciseTest, unittest.TestCase):
    """
    Unit tests for the `two-fer` analyzer.
    """
    @property
    def name(self):
        """
        Name of the exercise.
        """
        return "two-fer"

    def test_no_method(self):
        """
        Test marks missing `two_fer` method.
        """
        analysis = self.get_analysis("def ref_owt(): pass")
        self.assertIs(analysis.status, Status.DISAPPROVE_WITH_COMMENT)
        self.assertIn(self.comments.NO_METHOD, analysis.comment)
        self.assertIs(analysis.approved, False)

    def test_has_method(self):
        """
        Test no missing `two_fer` false positive.
        """
        analysis = self.get_analysis("def two_fer(): pass")
        self.assertNotIn(self.comments.NO_METHOD, analysis.comment)

    def test_simple_concat(self):
        """
        Test marks simple concatenation.
        """
        analysis = self.get_analysis(USES_CONCAT)
        self.assertIs(analysis.status, Status.REFER_TO_MENTOR)
        self.assertIn(self.comments.SIMPLE_CONCAT, analysis.comment)

    def test_no_simple_concat(self):
        """
        Test no simple concatenation false positive.
        """
        analysis = self.get_analysis(USES_STRING_FORMAT)
        self.assertNotIn(self.comments.SIMPLE_CONCAT, analysis.comment)

    def test_approves_optimal_string_format(self):
        """
        Test optimal solution that uses str.format.
        """
        analysis = self.get_analysis(USES_STRING_FORMAT)
        self.assertIs(analysis.status, Status.APPROVE_AS_OPTIMAL)
        self.assertIs(analysis.approved, True)
        self.assertFalse(analysis.comment)

    def test_approves_optimal_f_string(self):
        """
        Test optimal solution that uses f_strings.
        """
        analysis = self.get_analysis(USES_F_STRING)
        self.assertIs(analysis.status, Status.APPROVE_AS_OPTIMAL)
        self.assertIs(analysis.approved, True)
        self.assertFalse(analysis.comment)

    def test_no_def_arg(self):
        """
        Test marks missing default value.
        """
        analysis = self.get_analysis(NO_DEF_ARG)
        self.assertIs(analysis.status, Status.REFER_TO_MENTOR)
        self.assertIn(self.comments.NO_DEF_ARG, analysis.comment)

    def test_uses_def_args(self):
        """
        Test no missing default value false positive.
        """
        analysis = self.get_analysis(USES_STRING_FORMAT)
        self.assertNotIn(self.comments.NO_DEF_ARG, analysis.comment)

    def test_uses_conditionals(self):
        """
        Test marks use of conditionals.
        """
        analysis = self.get_analysis(USES_CONDITIONAL)
        self.assertIs(analysis.status, Status.REFER_TO_MENTOR)
        self.assertIn(self.comments.CONDITIONALS, analysis.comment)

    def test_no_conditionals(self):
        """
        Test no conditional use false positive.
        """
        analysis = self.get_analysis(USES_STRING_FORMAT)
        self.assertNotIn(self.comments.CONDITIONALS, analysis.comment)

    def test_no_return(self):
        """
        Test marks missing return statement.
        """
        analysis = self.get_analysis(NO_RETURN)
        self.assertIs(analysis.status, Status.DISAPPROVE_WITH_COMMENT)
        self.assertIn(self.comments.NO_RETURN, analysis.comment)
        self.assertIs(analysis.approved, False)

    def test_has_return(self):
        """
        Test no missing return statement false positive.
        """
        analysis = self.get_analysis(USES_STRING_FORMAT)
        self.assertNotIn(self.comments.NO_RETURN, analysis.comment)

    def test_wrong_def_arg(self):
        """
        Test marks incorrect default argument value.
        """
        analysis = self.get_analysis(WRONG_DEF_ARG)
        self.assertIs(analysis.status, Status.REFER_TO_MENTOR)
        self.assertIn(self.comments.WRONG_DEF_ARG, analysis.comment)

    def test_correct_def_arg(self):
        """
        Test no incorrect default argument value false positive.
        """
        analysis = self.get_analysis(USES_STRING_FORMAT)
        self.assertNotIn(self.comments.WRONG_DEF_ARG, analysis.comment)

    def test_uses_percent(self):
        """
        Test marks using percent string formatting.
        """
        analysis = self.get_analysis(USES_PERCENT)
        self.assertIs(analysis.status, Status.REFER_TO_MENTOR)
        self.assertIn(self.comments.PERCENT_FORMATTING, analysis.comment)

    def test_no_percent(self):
        """
        Test no percent string formatting false positive.
        """
        analysis = self.get_analysis(USES_STRING_FORMAT)
        self.assertNotIn(self.comments.PERCENT_FORMATTING, analysis.comment)


if __name__ == "__main__":
    unittest.main()
