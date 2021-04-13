"""
Classes for working with comments and comment types.
"""
from enum import Enum, unique
from dataclasses import dataclass, field, asdict



@unique
class BaseFeedback(Enum):
    """
    Superclass for all analyzers to user to build their Feedback.
    """

    def __new__(cls, namespace, comment):
        obj = object.__new__(cls)
        obj._value_ = f"python.{namespace}.{comment}".lower()
        return obj

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"



@unique
class CommentTypes(Enum):
    """
    Superclass for all analyzers to us for comment types
    """

    CELEBRATORY = 'celebratory'
    ESSENTIAL = 'essential'
    ACTIONABLE = 'actionable'
    INFORMATIVE = 'informative'

    def __str__(self):
        return self.value.lower()

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"


@dataclass
class Comment:
    comment: str = None
    params: dict = field(default_factory=dict)
    type:   Enum = CommentTypes.INFORMATIVE




@unique
class Summary(Enum):
    """
    Summary of the comments for the exercise under analysis.
    """

    CELEBRATE = "Congratulations!  This solution is very close to ideal!  We don't have any specific recommendations."
    REQUIRE = "There are a few changes we'd like you to make before completing this exercise."
    DIRECT = "There are a few changes we suggest that can bring your solution closer to ideal."
    INFORM = "Good work!  Here are some general recommendations for improving your Python code."
    GENERIC = "We don't have a custom analysis for thsi exercise yet, but here are some comments from PyLint to help you improve your code."

    def __str__(self):
        return self.value.lower()

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"