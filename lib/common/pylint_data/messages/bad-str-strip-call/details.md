A common misconception is that [str.strip('Hello')](https://docs.python.org/3.13/library/stdtypes.html#str.strip)
removes the *substring* `'Hello'` from the beginning and
end of the larger lstring. This is **not** the case. From the
[Python documentation](<https://docs.python.org/3/library/stdtypes.html?highlight=strip#str.strip>):

> _The chars argument is not a prefix or suffix; rather, **all
combinations of its values are stripped.**_

Duplicated characters in the [str.strip()](https://docs.python.org/3.13/library/stdtypes.html#str.strip) call, besides not
having any effect on the actual result, may indicate this
misunderstanding, and lead to future bugs.
