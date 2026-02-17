In Python 2.7, [super()]{.title-ref} has to be called with its own class
and [self]{.title-ref} as arguments ([super(Cat, self)]{.title-ref}),
which can lead to a mix up of parent and child class in the code.

In Python 3 the recommended way is to call [super()]{.title-ref}
[without]{#without} [arguments]() (see also
[super-with-arguments]{.title-ref}).

One exception is calling [super()]{.title-ref} on a non-direct parent
class. This can be used to get a method other than the default method
returned by the [mro()]{.title-ref}.
