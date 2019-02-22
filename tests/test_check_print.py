from unittest.mock import mock_open, patch

import pytest

from hulks.check_print import CheckPrintHook


@pytest.fixture
def hook():
    return CheckPrintHook()


@pytest.mark.parametrize('content', [
    'print()',
    "print('test')",
    'print("test")',
    'print ("test")',
    'print(some_variable)',
])
def test_check_print_validate_error(capsys, hook, content):
    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('whatever.py') is False
        mock_file.assert_called_once_with('whatever.py')

        output, _ = capsys.readouterr()

        assert output.startswith('whatever.py')
        assert 'line=1' in output


@pytest.mark.parametrize('content', [
    '_print()',
    "__print('test')",
    'print_something("test")',
    '_print ("test")',
    '_print(some_variable)',
])
def test_check_print_validate_pass(capsys, hook, content):
    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('whatever.py') is True
        mock_file.assert_called_once_with('whatever.py')

        output, _ = capsys.readouterr()
        assert '' in output


def test_check_print_inside_block_validate_error(capsys, hook):
    content = """
    \nclass Whatever:
        @classmethod
        def print_something(cls):
            print("something")

    \ndef print_something_two():
        print("something")

    \nif True:
        print("something")
    """
    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('whatever.py') is False
        mock_file.assert_called_once_with('whatever.py')

        output, _ = capsys.readouterr()

        assert output.startswith('whatever.py')
        assert 'line=6' in output
        assert 'line=10' in output
        assert 'line=14' in output


def test_check_print_inside_block_validate_pass(capsys, hook):
    content = """
    \nclass Whatever:
        @classmethod
        def print_something(cls):
            _print("something")

    \ndef print_something_two():
        print_foo("something")

    \nif True:
        __print("something")
    """
    with patch('builtins.open', mock_open(read_data=content)) as mock_file:
        assert hook.validate('whatever.py') is True
        mock_file.assert_called_once_with('whatever.py')

        output, _ = capsys.readouterr()
        assert '' in output
