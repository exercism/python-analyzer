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

    APPROVE = auto()
    DISAPPROVE = auto()
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

    def __init__(self, status, comment, pylint_comment, approvable=False):
        super(Analysis, self).__init__(
            status=status, comment=comment, pylint_comment=pylint_comment
        )
        self._approvable = approvable

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
    def approvable(self):
        """
        Is this analysis _considered_ approvable?
        Note that this does not imply an approved status, but that the exercise
        has hit sufficient points that a live Mentor would likely approve it.
        """
        return self._approvable

    @classmethod
    def approve(cls, comment=None, pylint_comment=None):
        """
        Create an Anaylsis that is approved.
        If non-optimal, comment should be a list of Comments.
        """
        return cls(
            Status.APPROVE, comment or [], pylint_comment or [], approvable=True
        )

    @classmethod
    def disapprove(cls, comment, pylint_comment=None):
        """
        Create an Analysis that is disapproved.
        """
        return cls(Status.DISAPPROVE, comment, pylint_comment or [])

    @classmethod
    def refer_to_mentor(cls, comment, pylint_comment=None, approvable=False):
        """
        Create an Analysis that should be referred to a mentor.
        """
        return cls(
            Status.REFER_TO_MENTOR, comment, pylint_comment or [], approvable=approvable
        )

    def dump(self, path: Path):
        """
        Dump's the current state to analysis.json.
        As a convenience returns the Anaylsis itself.
        """
        with open(path, "w") as dst:
            json.dump(self, dst, indent=4, cls=AnalysisEncoder)
        return self
