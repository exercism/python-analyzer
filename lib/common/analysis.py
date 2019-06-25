"""
Utility classes for analysis persistence.
"""

import json
from pathlib import Path
from enum import Enum, auto, unique
from typing import List

Comments = List[Enum]
PylintComments = List[str]


@unique
class Status(Enum):
    """
    Status of the exercise under analysis.
    """

    APPROVE_AS_OPTIMAL = auto()
    APPROVE_WITH_COMMENT = auto()
    DISAPPROVE_WITH_COMMENT = auto()
    REFER_TO_MENTOR = auto()

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


class AnalysisEncoder(json.JSONEncoder):
    """
    Simple encoder that will punt an Enum out as its string.
    """

    def default(self, obj):
        if isinstance(obj, Enum):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class Analysis(dict):
    """
    Represents the current state of the analysis of an exercise.
    """

    def __init__(self, status, comment, pylint_comment, approve=False):
        super(Analysis, self).__init__(
            status=status, comment=comment, pylint_comment=pylint_comment
        )
        self._approved = approve

    @property
    def status(self) -> Status:
        """
        The current status of the analysis.
        """
        return self["status"]

    @property
    def comment(self) -> Comments:
        """
        The list of comments for the analysis.
        """
        return self["comment"]

    @property
    def pylint_comment(self) -> PylintComments:
        """
        The list of pylint comments for the analysis.
        """
        return self["pylint_comment"]

    @property
    def approved(self):
        """
        Is this analysis _considered_ approve-able?
        Note that this does not imply an approved status, but that the exercise
        has hit sufficient points that a live Mentor would likely approve it.
        """
        return self._approved

    @classmethod
    def approve_as_optimal(cls, comment=None, pylint_comment=None):
        """
        Create an Anaylsis that is approved as optimal.
        """
        return cls(
            Status.APPROVE_AS_OPTIMAL, comment or [], pylint_comment or [], approve=True
        )

    @classmethod
    def approve_with_comment(cls, comment, pylint_comment=None):
        """
        Create an Analysis that is approved with comment.
        """
        return cls(
            Status.APPROVE_WITH_COMMENT, comment, pylint_comment or [], approve=True
        )

    @classmethod
    def disapprove_with_comment(cls, comment, pylint_comment=None):
        """
        Create an Analysis that is disapproved with comment.
        """
        return cls(Status.DISAPPROVE_WITH_COMMENT, comment, pylint_comment or [])

    @classmethod
    def refer_to_mentor(cls, comment, pylint_comment=None, approve=False):
        """
        Create an Analysis that should be referred to a mentor.
        """
        return cls(
            Status.REFER_TO_MENTOR, comment, pylint_comment or [], approve=approve
        )

    def dump(self, path: Path):
        """
        Dump's the current state to analysis.json.
        As a convenience returns the Anaylsis itself.
        """
        with open(path, "w") as dst:
            json.dump(self, dst, indent=4, cls=AnalysisEncoder)
        return self
