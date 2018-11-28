from io import BytesIO, StringIO
from unittest import mock

import pytest

from hulks.check_filename import BaseHook

SO_ERROR = 1
SO_SUCCESS = 0


class UnicodeErrorRaiserIO(BytesIO):
    def readlines(self, *args, **kwargs):
        for line in super().readlines(*args, **kwargs):
            yield line.decode('utf-8')

    __iter__ = readlines


@pytest.fixture
def hook():
    return BaseHook()


@pytest.fixture
def hook_iterator():
    class _TestHook(BaseHook):

        def validate(self, filename):
            lines = ''.join(line for _, line in self.lines_iterator(filename))
            print(lines)

            return True

    return _TestHook()


@pytest.fixture
def hook_with_option():
    class _TestHook(BaseHook):

        def add_arguments(self, parser):
            parser.add_argument('foobar')

    return _TestHook()


def test_base_handle(hook):
    mock_validate = mock.Mock(return_value=True)
    hook.validate = mock_validate

    args = ['file01.txt', 'another/file02.txt', 'file03.txt']

    result = hook.handle(args)
    assert result == SO_SUCCESS
    assert mock_validate.call_count == 3


def test_base_handle_failure(hook):
    mock_validate = mock.Mock(side_effect=lambda filename: filename != 'file03.txt')
    hook.validate = mock_validate

    args = ['file01.txt', 'another/file02.txt', 'file03.txt']

    result = hook.handle(args)
    assert result == SO_ERROR
    assert mock_validate.call_count == 3


def test_base_handle_multiple_failure(hook):
    mock_validate = mock.Mock(side_effect=lambda filename: filename != 'file01.txt')
    hook.validate = mock_validate

    args = ['file01.txt', 'another/file02.txt', 'file03.txt']

    result = hook.handle(args)
    assert result == SO_ERROR
    assert mock_validate.call_count == 3


def test_base_handle_calls(hook):
    hook.validate = mock.Mock(return_value=True)
    result = hook.handle(['foobar.txt'])
    hook.validate.assert_called_once_with('foobar.txt')
    assert result == SO_SUCCESS


def test_base_handle_calls_with_option(hook_with_option):
    hook_with_option.validate = mock.Mock(return_value=True)
    result = hook_with_option.handle(['foobar.txt', 'flango'])
    hook_with_option.validate.assert_called_once_with('foobar.txt', foobar='flango')
    assert result == SO_SUCCESS


def test_lines_iterator(hook_iterator, capsys):
    with mock.patch('hulks.base.open') as mocked_open:
        mocked_open.return_value = StringIO('some text\nmore text')

        result = hook_iterator.validate('whatever.txt')

    output, _ = capsys.readouterr()
    lines = output.split('\n')
    # there's an extra newline added by "print" statement
    assert len(lines) == 3
    assert lines[0] == 'some text'
    assert lines[1] == 'more text'
    assert lines[2] == ''
    assert result is True


def test_lines_iterator_line_number(hook_iterator, capsys):
    with mock.patch('hulks.base.open') as mocked_open:
        mocked_open.return_value = StringIO('some text\nmore text')
        line_numbers = [lino for lino, _ in hook_iterator.lines_iterator('whatever.txt')]

    assert line_numbers == [1, 2]


def test_lines_iterator_noqa(hook_iterator, capsys):
    with mock.patch('hulks.base.open') as mocked_open:
        mocked_open.return_value = StringIO('some text # noqa\nmore text')

        result = hook_iterator.validate('whatever.txt')

    output, _ = capsys.readouterr()
    lines = output.split('\n')
    # there's an extra newline added by "print" statement
    assert len(lines) == 2
    assert lines[0] == 'more text'
    assert lines[1] == ''
    assert result is True


@mock.patch('hulks.base.open')
def test_lines_iterator_prints_filename_on_invalid_files(mocked_open, hook_iterator):
    mocked_open.return_value = UnicodeErrorRaiserIO(b'This is invalid utf-8:\xfe\xfe!')
    with pytest.raises(UnicodeDecodeError) as excinfo:
        hook_iterator.validate('whatever.png')

    assert "at file 'whatever.png'" in str(excinfo.value)
