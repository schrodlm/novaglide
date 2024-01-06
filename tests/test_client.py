from pylint.lint import Run
from pylint.reporters import CollectingReporter
import pytest

# code style tests copied from the homeworks


@pytest.fixture(scope="session")
def linter():
    """ Test codestyle for src file of render_tree fucntion. """
    src_file = "src/*.py"
    rep = CollectingReporter()
    # disabled warnings:
    # 0301 line too long
    # 0103 variables name (does not like shorter than 2 chars)
    r = Run(['--disable=C0301,C0103,', '-sn', src_file],
            reporter=rep, exit=False)
    return r.linter


@pytest.mark.parametrize("limit", range(0, 11))
def test_codestyle_score(linter, limit, runs=[]):
    """ Evaluate codestyle for different thresholds. """
    if len(runs) == 0:
        print('\nLinter output:')
        for m in linter.reporter.messages:
            print(f'{m.msg_id} ({m.symbol}) line {m.line}: {m.msg}')
    runs.append(limit)
    # score = linter.stats['global_note']
    score = linter.stats.global_note

    print(f'pylint score = {score} limit = {limit}')
    assert score >= limit
