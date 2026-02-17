Directly asserting a string literal will always pass. The solution is to
test something that could fail, or not assert at all.

For assertions using `assert` there are similar messages:
`assert-on-string-literal`{.interpreted-text role="ref"} and
`assert-on-tuple`{.interpreted-text role="ref"}.
