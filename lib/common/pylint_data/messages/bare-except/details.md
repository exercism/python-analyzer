A good rule of thumb is to limit use of bare 'except' clauses to two
cases: 1. If the exception handler will be printing out or logging the
traceback; at least the user will be aware that an error has occurred.
2. If the code needs to do some cleanup work, but then lets the
exception propagate upwards with raise. [try\...finally]{.title-ref} can
be a better way to handle this case.
