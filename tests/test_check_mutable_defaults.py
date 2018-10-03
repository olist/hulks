from unittest.mock import mock_open, patch

import pytest

from hulks.check_mutable_defaults import CheckMutableDefaults


@pytest.fixture
def hook():
    return CheckMutableDefaults()


@pytest.mark.parametrize('content', [
    'def foo(var=[]): pass',
    'def foo(var={}): pass',
    'def foo(var=set()): pass',
    'def foo(var=list()): pass',
    'def foo(var=dict()): pass',
    'def foo(var=TypeError()): pass',
])
def test_function_with_mutable_default(capsys, hook, content):
    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is False
        mock_file.assert_called_once_with('foo.py')

        output, _ = capsys.readouterr()
        assert '(foo)' in output


@pytest.mark.parametrize('mutable_arg', ['[]', '{}', 'set()', 'list()', 'dict()', 'ValueError()'])
def test_method_with_mutable_default(capsys, hook, mutable_arg):
    content = """
    \nclass A:
        def foo(self, arg={}):
            pass
    """.format(mutable_arg)

    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is False
        mock_file.assert_called_once_with('foo.py')

        output, _ = capsys.readouterr()
        assert '(foo)' in output


def test_immutable_default(capsys, hook):
    content = """
    \ndef foo(arg0='', arg1=1, arg2=None, arg3=tuple(), arg4=object()):
        pass
    """

    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is True
        mock_file.assert_called_once_with('foo.py')

        output, _ = capsys.readouterr()
        assert output == ""
