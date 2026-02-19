"""
Analyzer for the `two-fer` exercise.
"""
import ast
from io import StringIO
from pylint.lint import Run
from pathlib import Path


from common import Analysis, BaseFeedback, Summary
from common.comment import Comment, CommentTypes
from common.pylint_comments import generate_pylint_comments



class Comments(BaseFeedback):
    NO_MODULE = ("general", "no_module")
    NO_METHOD = ("two-fer", "no_method")
    MALFORMED_CODE = ("general", "malformed_code")
    SIMPLE_CONCAT = ("two-fer", "simple_concat")
    NO_DEF_ARG = ("two-fer", "no_def_arg")
    CONDITIONALS = ("two-fer", "conditionals")
    NO_RETURN = ("two-fer", "no_return")
    WRONG_DEF_ARG = ("two-fer", "wrong_def_arg")
    PERCENT_FORMATTING = ("two-fer", "percent_formatting")



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

    # Does the solution have a method called two_fer?
    has_method = False

    # Does the solution correctly use a default argument?
    uses_def_arg = False

    # Does the solution have a return value?
    has_return = False

    # Does the solution use str.format?
    uses_format = False

    # Does the solution use f-strings?
    uses_f_string = False

    for node in ast.walk(tree):

        # Check for method called two_fer
        if isinstance(node, ast.FunctionDef):
            has_method = node.name == "two_fer"

        # Check for the use of string concatenation with + operator
        elif isinstance(node, ast.Add) and Comments.SIMPLE_CONCAT not in comments:
            comments.append(Comment(type=CommentTypes.ACTIONABLE, params={}, comment=Comments.SIMPLE_CONCAT))

        # Check for use of default arguments
        elif isinstance(node, ast.arguments):
            if node.defaults:
                uses_def_arg = True
                # Check if the default argument use is correct
                try:
                    if (node.defaults[0].s != "you" and Comments.WRONG_DEF_ARG not in comments):
                        comments.append(Comment(type=CommentTypes.ESSENTIAL, params={}, comment=Comments.WRONG_DEF_ARG))
                except Exception:
                    if Comments.WRONG_DEF_ARG not in comments:
                        comments.append(Comment(type=CommentTypes.ESSENTIAL, params={}, comment=Comments.WRONG_DEF_ARG))

        # Check for use of unnecessary conditionals
        elif isinstance(node, ast.If) and Comments.CONDITIONALS not in comments:
            comments.append(Comment(type=CommentTypes.ACTIONABLE, params={}, comment=Comments.CONDITIONALS))

        # Check for use of %-formatting
        elif isinstance(node, ast.Mod) and Comments.PERCENT_FORMATTING not in comments:
            comments.append(Comment(type=CommentTypes.ACTIONABLE, params={}, comment=Comments.PERCENT_FORMATTING))

        # Check for a return statement
        elif isinstance(node, ast.Return):
            has_return = True

        # Search for use of str.format
        elif isinstance(node, ast.Call):
            try:
                uses_format = node.func.attr == "format"
            except Exception:
                pass

        # Search for use of f-strings
        try:
            if isinstance(node, ast.FormattedValue):
                uses_f_string = True
        except AttributeError:
            pass  # Fail if python version is too low

    if not has_method:
        comments.append(Comment(type=CommentTypes.ESSENTIAL, params={}, comment=Comments.NO_METHOD))

    if not uses_def_arg:
        comments.append(Comment(type=CommentTypes.ESSENTIAL, params={}, comment=Comments.NO_DEF_ARG))

    if not has_return:
        comments.append(Comment(type=CommentTypes.ESSENTIAL, params={}, comment=Comments.NO_RETURN))


    # Generate PyLint comments for additional feedback.
    comments.extend(generate_pylint_comments(in_path))


    # Process all comments and write out feedback.
    if uses_format or uses_f_string:
        return Analysis.summarize_comments(comments, output_file, ideal=True)
    else:
        return Analysis.summarize_comments(comments, output_file)
