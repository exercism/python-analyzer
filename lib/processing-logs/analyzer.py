"""
Analyzer for the `cater-waiter` exercise.
"""

import ast

from io import StringIO
from pylint.lint import Run
from pylint import run_pylint
from pathlib import Path
from pylint.reporters.text import TextReporter

from common import Analysis, BaseFeedback, Summary
from common.comment import Comment, CommentTypes
from common.pylint_comments import generate_pylint_comments


class Comments(BaseFeedback):
    NO_MODULE = ("general", "no_module")
    NO_METHOD = ("two-fer", "no_method")
    NO_RETURN = ("general", "no_return")
    MALFORMED_CODE = ("general", "malformed_code")
    GENERAL_RECS = ("general", "general_recommendations")


def analyze(in_path: Path, out_path: Path):
    """
    Analyze the user's Two Fer solution to give feedback. Outputs a JSON that

    conforms to https://github.com/exercism/docs/blob/main/building/tooling/analyzers/interface.md#output-format
    """

    # List of Comment objects to process
    comments = []

    output_file = out_path.parent.joinpath("analysis.json")

    # input file - if it can't be found, fail and bail
    try:
        user_solution = in_path.read_text()
    except OSError as err:
        # fail out fast with an ESSENTIAL (required) type comment for the student
        comments.append(Comment(type=CommentTypes.ESSENTIAL, params={}, comment=Comments.MALFORMED_CODE))
    finally:
        if comments:
            return Analysis.require(comments).dump(output_file)

    # AST - if an AST can't be made, fail and bail
    try:
        tree = ast.parse(user_solution)
    except Exception:
        # If ast.parse fails, assume malformed code and fail with an ESSENTIAL (required) type comment for the student
        comments.append(Comment(type=CommentTypes.ESSENTIAL, params={}, comment=Comments.MALFORMED_CODE))
    finally:
        if comments:
            return Analysis.require(comments).dump(output_file)

    # Generate PyLint comments for additional feedback.
    comments.extend(generate_pylint_comments(in_path))

     # If there are no comments, add the general recommendations as comments.
    if not comments:
        comments.append(Comment(type=CommentTypes.INFORMATIVE, params={}, comment=Comments.GENERAL_RECS))

    return Analysis.summarize_comments(comments, output_file)
