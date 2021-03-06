import pytest
import os

pytest_plugins = ["pytester"]


@pytest.fixture
def path():
    return os.path.dirname(os.path.dirname(__file__))


@pytest.fixture
def run(testdir, path):
    def do_run(*args):
        args = [
            "python", "-m", "simuling"] + list(args)
        return testdir._run(*args)
    return do_run


def test_does_run(tmpdir, run):
    import json
    os.mkdir("Data")
    input = tmpdir.join("example.json")
    json.dump(
        {'population_graph': 'krackhardt',
         'time_steps': 0},
        # Because we don't test output, don't run the simulation so
        # as to not pretend too high coverage.
        input.open("w"))
    result = run(input)
    assert result.ret == 0


def test_bad_graph_model(tmpdir, run):
    import json
    os.mkdir("Data")
    input = tmpdir.join("example.json")
    json.dump(
        {'population_graph': '\u1234',
         'time_steps': 500},
        input.open("w"))
    result = run(input)
    assert result.ret == 1
