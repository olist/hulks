from unittest import mock

import pytest

from hulks.check_invalid_domains import InvalidDomainsHook


@pytest.fixture
def hook():
    return InvalidDomainsHook()


def test_invalid_domains_validate(capsys, hook):
    hook.lines_iterator = mock.Mock(return_value=[(1, "https://foobar.herokuapp.com")])
    result = hook.validate("whatever.txt")

    output, _ = capsys.readouterr()
    hook.lines_iterator.assert_called_once_with("whatever.txt")
    assert output.startswith("whatever.txt")
    assert "line=1" in output
    assert "column=1" in output
    assert result is False


def test_invalid_domains_validate_unmatch(capsys, hook):
    hook.lines_iterator = mock.Mock(return_value=[(1, "https://foobar.localhost.com")])
    result = hook.validate("whatever.txt")
    output, _ = capsys.readouterr()
    hook.lines_iterator.assert_called_once_with("whatever.txt")
    assert output == ""
    assert result is True
