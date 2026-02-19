# The try except might be removed entirely:
1 / 0


# Another more detailed exception can be raised:
try:
    1 / 0
except ZeroDivisionError as e:
    raise ValueError("The area of the rectangle cannot be zero") from e
