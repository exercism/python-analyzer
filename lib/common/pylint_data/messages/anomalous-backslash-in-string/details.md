`\z` is same as `\\z` because there is no escape sequence for `z`.
But that is not clear for the reader of the code.

The only reason this is demonstrated to raise `syntax-error` is because pylint's CI now runs on Python 3.12, where this truly raises a `SyntaxError`.
We hope to address this discrepancy in the documentation in the future.

