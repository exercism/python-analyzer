# Exercism's Python Analyzer

This is Exercism's automated analyzer for the Python track.

It is run with `./bin/run.sh $EXERCISM $PATH_TO_FILES $PATH_FOR_OUTPUT` and will read the source code from `$PATH_TO_FILES` and write a text file with an analysis to `$PATH_FOR_OUTPUT`.

For example:

```bash
./bin/run.sh two_fer ~/solution-238382y7sds7fsadfasj23j/ ~/solution-238382y7sds7fsadfasj23j/output/
```

Unit tests can be run from this directory:

```bash
pytest -x
```
