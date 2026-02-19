Directly asserting a string literal will always pass.
The fix is to test something that could fail, or not assert at all.

For `unittest` assertions there is the similar `redundant-unittest-assert` message.
