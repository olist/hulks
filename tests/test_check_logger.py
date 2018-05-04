from unittest import mock

import pytest

from hulks.check_logger import CheckLoggerHook


@pytest.fixture
def hook():
    return CheckLoggerHook()


@pytest.mark.parametrize('text', [
    'logger = logging.getLogger(__file__)',
    'logger = logging.getLogger(__main__)',
    'logger = logging.getLogger(var)',
    'logger = logging.getLogger()',
])
def test_check_logger_validate_error(capsys, hook, text):
    hook.lines_iterator = mock.Mock(
        return_value=[(1, text)]
    )
    result = hook.validate('whatever.txt')

    output, _ = capsys.readouterr()
    assert hook.lines_iterator.called_once_with('whatever.txt')
    assert output.startswith('whatever.txt')
    assert 'line=1' in output
    assert result is False


@pytest.mark.parametrize('text', [
    'logger = logging.getLogger(__name__)',
    'logger = getLogger(__name__)',
    'logger = getLogger("custom")',
    "logger = getLogger('custom')",
])
def test_check_logger_validate_pass(capsys, hook, text):
    hook.lines_iterator = mock.Mock(
        return_value=[(1, text)]
    )
    result = hook.validate('whatever.txt')
    output, _ = capsys.readouterr()
    assert hook.lines_iterator.called_once_with('whatever.txt')
    assert output == ''
    assert result is True
