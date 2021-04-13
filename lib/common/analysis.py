"""
Utility classes for analysis persistence.
"""

import json
from pathlib import Path
from enum import Enum
from dataclasses import asdict, is_dataclass
from common.comment import Summary


class AnalysisEncoder(json.JSONEncoder):
    """
    Simple encoder that will punt an Enum out as its string.
    """

    def default(self, obj):
        if isinstance(obj, Enum):
            return str(obj)

        elif is_dataclass(obj):
            return asdict(obj)

        return json.JSONEncoder.default(self, obj)


class Analysis(dict):
    """
    Represents the current state of the analysis of an exercise.
    """

    def __init__(self, summary, comments):
        super(Analysis, self).__init__(summary=summary, comments=comments)


    @property
    def summary(self) -> Summary:
        """
        The current summary of the analysis.
        """

        return self["summary"]

    @property
    def comment(self):
        """
        The list of comments for the analysis.
        """
        return self["comments"]

    @classmethod
    def celebrate(cls,  comments=None):
        """
        Create an Anaylsis that is approved.
        If non-optimal, comment should be a list of Comments.
        """
        return cls(Summary.CELEBRATE, comments or [])


    @classmethod
    def require(cls, comments):
        """
        Create an Analysis that is disapproved.
        """
        return cls(Summary.REQUIRE, comments)

    @classmethod
    def direct(cls, comments):
        """
        Create an Analysis that should be referred to a mentor.
        """
        return cls(Summary.DIRECT, comments)

    @classmethod
    def inform(cls, comments, pylint_comment=None):
        return cls(Summary.INFORM, comments)


    def dump(self, out_path: Path):
        """
        Dump's the current state to analysis.json.
        As a convenience returns the Anaylsis itself.
        """
        with open(out_path, "w") as dst:
            json.dump(self, dst, indent=4, cls=AnalysisEncoder)
        return self
