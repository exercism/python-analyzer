from common.comment import Comment, CommentTypes
from pylint import epylint as lint
from pathlib import Path


def generate_pylint_comments(in_path):
    '''
        Use Pylint to generate additional feedback comments for code,

        e.g. if code follows PEP8 Style Convention
    '''

    pylint_stdout, _ = lint.py_run(
        str(in_path) + ' --score=no --msg-template="{category}, {line}, {msg_id} {symbol}, {msg}"',
        return_std=True
    )

    status_mapping = {
        'informational': CommentTypes.INFORMATIVE,
        'refactor' :  CommentTypes.ACTIONABLE,
        'convention' : CommentTypes.ACTIONABLE,
        'warning' : CommentTypes.ESSENTIAL,
        'error' : CommentTypes.ESSENTIAL,
        'fatal' : CommentTypes.ESSENTIAL
    }

    cleaned_pylint_output = [tuple(item.strip('" ').split(', '))
                             for item in pylint_stdout.getvalue().splitlines()
                             if '**' not in item]

    pylint_comments = []

    for line in cleaned_pylint_output:
        if line[0]:
            if line[2] == "C0301 line-too-long":
                continue

            if line[2] in ("C0114 missing-module-docstring",
                           "C0116 missing-function-docstring",
                           "C0304 missing-final-newline"):

                pylint_comments.append(Comment(type=status_mapping['informational'],
                                               params={'lineno': line[1], 'code': line[2], 'message': line[3:]},
                                               comment=f'python.pylint.{line[0]}'))
            else:
                pylint_comments.append(Comment(type=status_mapping[line[0]],
                                               params={'lineno': line[1], 'code': line[2], 'message': line[3:]},
                                               comment=f'python.pylint.{line[0]}'))

    return pylint_comments
