"""
Run tests on the analyzer itself.
"""


import json
import os
import subprocess
import tempfile
from pathlib import Path

import pytest


ROOT = Path(__file__).parent
ANALYZER = ROOT.joinpath("..", "bin", "run.sh").resolve(strict=True)
TESTS = sorted(ROOT.glob("*/*.py"))

def run_in_subprocess(test_path, golden_path, args=None):
    """
    Run given tests against the given golden file.
    """

    exercise_dir = test_path.parent
    exercise_name = exercise_dir.name

    with tempfile.TemporaryDirectory(prefix="test-analyzer-tests", dir=ROOT) as tmp_dir:
        rc = subprocess.run([ANALYZER, exercise_name, exercise_dir, tmp_dir]).returncode

        analysis_json = Path(tmp_dir).joinpath("analysis.json").resolve(strict=True)

        return (json.loads(analysis_json.read_text()), json.loads(golden_path.read_text())), rc


@pytest.fixture(params=TESTS, ids=(os.path.split(path)[0].split("/")[-1] for path in TESTS))
def test_with_golden(request):
    """
    Path to a test and its golden files.
    """

    path = request.param
    golden_analysis = path.parent.joinpath("analysis.json").resolve(strict=True)

    return (path, golden_analysis)


def test_results_matches_golden_file(test_with_golden):
    """
    Test that the results of a run matches the golden file.
    """

    run_results, rc = run_in_subprocess(*test_with_golden)
    current_run, golden = run_results

    assert current_run == golden, "results must match the golden file"
    assert rc == 0, f"return code must be 0 even when errors occur: got {rc}"
