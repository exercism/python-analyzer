Shadowing [built-ins](https://docs.python.org/3.13/library/functions.html) at the global scope is discouraged because it
obscures their behavior throughout the entire module, increasing the
risk of subtle bugs when the built-in is needed elsewhere.

 In contrast, local redefinitions _might_ be acceptable as their impact is confined to a
specific scope; although it is generally not a good idea.
