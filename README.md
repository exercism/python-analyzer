# Exercism's Python Analyzer

This is Exercism's automated analyzer for the Python track exercises.
It is based on and uses [PyLint][pylint-github].

It is run from a docker container using `./bin/run-in-docker.sh $EXERCISE_SLUG $PATH_TO_SOLUTION_FILES $PATH_FOR_OUTPUT_FILES` and will read the source code from `$PATH_TO_SOLUTION_FILES` and write a json file with an analysis to `$PATH_FOR_OUTPUT_FILES`.
Please note `$PATH_TO_SOLUTION_FILES` and `$PATH_FOR_OUTPUT_FILES` need to be **_relative_** to the location of this repo in your environment.

For example:

```bash
# From python-analyzer (project root) directory
./bin/run-in-docker.sh two_fer ~/solution-238382y7sds7fsadfasj23j/ ~/solution-238382y7sds7fsadfasj23j/output/
```

Or if you also have the Python content repo cloned alongside this repo and have a solution saved in the stub file:

```bash
# From python-analyzer (project root) directory
./bin/run-in-docker.sh two_fer ../python/exercises/practice/two-fer/ ../python/exercises/practice/two-fer/
```


## Running the Tests for the Analyzer

Unit tests require [docker][docker] and can be run locally or from within GitHub via [codespaces][codespaces]:

1,  Build the analyzer image from the Dockerfile
2.  Open a terminal in the root of your copy/local copy of this project.
3.  run
    ```bash
    #run from the python-analyzer (project root) directory.
    ./bin/run-tests-in-docker.sh
    ```

> [!NOTE]
> The PyLint portion of the Analyzer will respect the `# pylint: disable=<rule_id>`, `# pylint: disable-next=<rule_id>`, and `# pylint: disable=all` directives from within code files, but it is recommended that you use them sparingly.

> For more details on PyLint message control, see [message_control](https://pylint.pycqa.org/en/latest/user_guide/messages/message_control.html#block-disables).


[pylint-github]: https://github.com/pylint-dev/pylint
[docker]: https://www.docker.com/
[codespaces]: https://github.com/features/codespaces
