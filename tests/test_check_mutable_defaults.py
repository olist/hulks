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


@pytest.mark.parametrize('content', [
    'def foo(var=(None, [])): pass',
    'def foo(var=({None, []})): pass',
    'def foo(var=(None, set())): pass',
    'def foo(var=(None, list())): pass',
    'def foo(var=(None, dict())): pass',
    'def foo(var=(None, TypeError())): pass',
])
def test_function_with_nested_mutable_default(capsys, hook, content):
    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is False

    mock_file.assert_called_once_with('foo.py')

    output, _ = capsys.readouterr()
    assert '(foo)' in output


@pytest.mark.parametrize('content', [
    'async def foo(var=[]): pass',
    '@asyncio.coroutine\ndef foo(var={}): pass',
    '@types.coroutine\ndef foo(var=set()): pass',
])
def test_async_function_with_mutable_default(capsys, hook, content):
    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is False
        mock_file.assert_called_once_with('foo.py')

        output, _ = capsys.readouterr()
        assert '(foo)' in output


def test_functions_with_mutable_default(capsys, hook):
    content = """
    \ndef foo(arg=[]):
          pass

    \ndef bar(arg=None):
        pass
    """

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


def test_dunder_method_with_mutable_default(capsys, hook):
    content = """
    \nclass A:
        def __init__(self, arg={}):
            pass
    """.format([])

    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is False
        mock_file.assert_called_once_with('foo.py')

        output, _ = capsys.readouterr()
        assert '(__init__)' in output


@pytest.mark.parametrize('mutable_arg', ['[]', '{}', 'set()', 'list()', 'dict()', 'ValueError()'])
def test_async_method_with_mutable_default(capsys, hook, mutable_arg):
    content = """
    \nclass A:
        async def foo(self, arg={}):
            pass
    """.format(mutable_arg)

    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is False
        mock_file.assert_called_once_with('foo.py')

        output, _ = capsys.readouterr()
        assert '(foo)' in output


@pytest.mark.parametrize('prefix', ['', 'async ', '@asyncio.coroutine\n'])
def test_immutable_default(capsys, hook, prefix):
    content = """
    \n{}def foo(arg0='', arg1=1, arg2=None, arg3=tuple(), arg4=object()):
        pass
    """.format(prefix)

    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is True
        mock_file.assert_called_once_with('foo.py')

        output, _ = capsys.readouterr()
        assert output == ""


def test_class_attribute_with_immutable_default(capsys, hook):
    content = """
    \nclass A:
        foo = None

    \nclass B:
        baz = None
    """

    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is True
        mock_file.assert_called_once_with('foo.py')

        output, _ = capsys.readouterr()
        assert output == ""


@pytest.mark.parametrize('mutable_arg', ['[]', '{}', 'set()', 'list()', 'dict()', 'ValueError()'])
def test_class_attribute_with_mutable_default(capsys, hook, mutable_arg):
    content = """
    \nclass A:
        foo = None

    \nclass B:
        bar = {}
        baz = None
    """.format(mutable_arg)

    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is False
        mock_file.assert_called_once_with('foo.py')

        output, _ = capsys.readouterr()
        assert '(bar)' in output


def test_annotated_class_attribute_with_mutable_default(capsys, hook):
    content = """
    \nclass A:
        foo = None

    \nclass B:
        bar: typing.List[str] = []
        baz = None
    """

    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('foo.py') is False
        mock_file.assert_called_once_with('foo.py')

        output, _ = capsys.readouterr()
        assert '(bar)' in output
