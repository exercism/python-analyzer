"""
Classes for working with comments.
"""
from enum import Enum, unique


@unique
class BaseComments(Enum):
    """
    Superclass for all analyzers to user to build their Comments.
    """

    def __new__(cls, namespace, comment):
        obj = object.__new__(cls)
        obj._value_ = f"python.{namespace}.{comment}".lower()
        return obj

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
