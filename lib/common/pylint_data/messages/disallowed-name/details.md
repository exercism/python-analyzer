## Good names:

1. Follow existing naming conventions for the codebase or framework you are working in, and are in the language (_e.g. Spanish, French, English_) that the codebase or framework uses.
2. Are clear and concise.
3. Are as long as necessary to communicate, but no longer.
   - It is OK to be verbose, but it has gone too far if the variable name is so long that it starts to interfere with easily reading the code.
4. Avoid the use of single letters or frequent abbreviations.
   - Err on the side of being descriptive. Other programmers (and your future self) will thank you for your clarity.
   - Remember that context _matters_.  The context of your variable (or function or class) name is likely to be lost if the code is longer than about 5 lines.  Even within that 5-line limit, those reading your code for the first time might have difficulty following.
   - The memory/time saved in typing something short but obscure is more than negated by someone not understanding the code at first glance.
5. Avoid what is known as [Hungarian notation](https://en.wikipedia.org/wiki/Hungarian_notation), especially _systems Hungarian notation_.
   - Naming something `time_in_minutes` (_if it is needed for clarity in your program_) is OK, but not `time_in_minutes_object` (_if you are already using a `time` or `datetime` object_).
   - Naming something results is OK, but `results_list` is not good (_especially if there is a chance that the variable could be reassigned as a `tuple` or `set`, or that the function or class name could contradict the return type._)
6. Do not conflict with any [Python keywords](https://docs.python.org/3/reference/lexical_analysis.html#keywords) or [Python soft keywords](https://docs.python.org/3/reference/lexical_analysis.html#soft-keywords), These are reserved for special operations in Python and cannot be used as variable names.
7. Do not conflict with/shadow any [Python built in names](https://docs.python.org/3/library/functions.html).
