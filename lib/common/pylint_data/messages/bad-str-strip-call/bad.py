"Hello World".strip("Hello")  # [bad-str-strip-call - the l is repeated]
# >>> ' World'

"abcbc def bacabc".strip("abcbc ")  # [bad-str-strip-call - b and c are repeated]
# >>> 'def'