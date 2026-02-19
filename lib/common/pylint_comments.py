"""Functions for providing PyLint feedback.."""

from common.comment import Comment, CommentTypes
from io import StringIO
from pylint.lint import Run
from pylint import run_pylint
from pathlib import Path
from pylint.reporters.text import TextReporter


def find_pylint_rule_details(path):
    """Find Pylint extended feedback by rule."""

    file_path = Path(path)

    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        return None

    return content


def generate_pylint_comments(in_path, pylint_spec='/opt/analyzer/lib/common/.pylintrc'):
    """Use Pylint to generate additional feedback comments for code.

        e.g. if code follows PEP8 Style Convention
    """

    status_mapping = {
        'informational': CommentTypes.INFORMATIVE,
        'refactor' :  CommentTypes.ACTIONABLE,
        'convention' : CommentTypes.ACTIONABLE,
        'warning' : CommentTypes.ESSENTIAL,
        'error' : CommentTypes.ESSENTIAL,
        'fatal' : CommentTypes.ESSENTIAL
    }

    pylint_output = StringIO()
    reporter = TextReporter(pylint_output)
    template = '--msg-template="{category}, {line}, {msg_id} {symbol}, {msg}"'
    rcfile = f'--rcfile={pylint_spec}'
    cmnd_line_options = [f"{str(in_path)}", rcfile, "--score=n", f"{template}"]
    messages_path = '/opt/analyzer/lib/common/pylint_data/messages'

    Run(cmnd_line_options, reporter=reporter, exit=False)

    cleaned_pylint_output = (tuple(item.strip('" ').split(', '))
                             for item in pylint_output.getvalue().splitlines()
                             if '**' not in item)

    pylint_comments = []

    for line in cleaned_pylint_output:
        if line[0]:
            rule_name = line[2][6:]
            bad = find_pylint_rule_details(path=f"{messages_path}/{rule_name}/bad.py")
            good = find_pylint_rule_details(path=f"{messages_path}/{rule_name}/good.py")
            related = find_pylint_rule_details(path=f"{messages_path}/{rule_name}/related.md")
            details = find_pylint_rule_details(path=f"{messages_path}/{rule_name}/details.md")

            if not line[2] or line[2] == "C0301 line-too-long":
                continue

            if line[2] in {"C0114 missing-module-docstring",
                           "C0116 missing-function-docstring",
                           "C0304 missing-final-newline"}:

                status_type = status_mapping['informational']
            else:
                status_type = status_mapping[line[0]]

            pylint_comments.append(Comment(type=status_type,
                                           params={'lineno': line[1],
                                                   'code': line[2],
                                                   'message': ', '.join(line[3:]),
                                                   'bad_code': f'Instead of: \n```python\n{bad}```\n\n' if bad else None,
                                                   'good_code': f'Try: \n```python\n{good}```\n\n' if good else None,
                                                   'related_info': related,
                                                   'details': details},
                                           comment=f'python.pylint.{line[0]}'))

    return pylint_comments
