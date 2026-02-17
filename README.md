# Exercism's Python Analyzer

This is Exercism's automated analyzer for the Python track exercises.
It is based on and uses [PyLint][pylint-github].

It is run from a docker container using `./bin/run-in-docker.sh $EXERCISM $PATH_TO_FILES $PATH_FOR_OUTPUT` and will read the source code from `$PATH_TO_FILES` and write a text file with an analysis to `$PATH_FOR_OUTPUT`.

For example:

```bash
./bin/run-in-docker.sh two_fer ~/solution-238382y7sds7fsadfasj23j/ ~/solution-238382y7sds7fsadfasj23j/output/
```

Unit tests also require [docker][docker] and can be run locally or from within GitHub via [codespaces][codespaces]:

```bash

#run from the python-analyzer (project root) directory.
./bin/run-tests-in-docker.sh
```

[pylint-github]: https://github.com/pylint-dev/pylint
[docker]: https://www.docker.com/
[codespaces]: https://github.com/features/codespaces
