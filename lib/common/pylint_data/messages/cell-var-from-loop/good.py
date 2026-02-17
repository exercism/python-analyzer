def teacher_greeting(names):
    def greet(name):
        # do something
        print(f"Hello, {name}!")

    for name in names:
        if name.isalpha():
            # we're passing the value of "name" to the function here
            greet(name)


teacher_greeting(["Graham", "John", "Terry", "Eric", "Terry", "Michael"])

###

import functools


def teacher_greeting(names):
    greetings = []
    for name in names:
        if name.isalpha():
            # "name" is evaluated when the partial is created here, so this
            # does not do lazy evaluation
            greetings.append(functools.partial(print, f"Hello, {name}!"))

    for greet in greetings:
        # `partial`s are called like functions, but you've already passed the
        # arguments to them
        greet()


teacher_greeting(["Graham", "John", "Terry", "Eric", "Terry", "Michael"])
