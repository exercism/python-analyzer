In Python 2.7, [super()](https://docs.python.org/2.7/library/functions.html#super) has to be called with its own class
and `self` as arguments ([super(Cat, self)](https://docs.python.org/2.7/library/functions.html#super)),
which can lead to a mix-up of parent and child class in the code.

In Python 3 the recommended way is to call [super()](https://docs.python.org/3/library/functions.html#super) _without_
[arguments](https://docs.python.org/3/glossary.html#term-argument) (see also
[super-considered-super](https://rhettinger.wordpress.com/2011/05/26/super-considered-super/)).

One exception is calling `super()` on a non-direct parent
class. This can be used to get a method other than the default method
returned by the [mro()](https://docs.python.org/3/glossary.html#term-method-resolution-order).
