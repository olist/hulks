import pytest

from hulks.check_filename import FilenameHook


@pytest.fixture
def hook():
    return FilenameHook()


@pytest.mark.parametrize(
    "filename",
    [
        "escaped file",
        "invalid-python-file.py",
        "invalid_web_file.html",
        "another_web_file.htm",
        "yet_another_web_file.css",
        "just_this_other_web_file.js",
    ],
)
def test_filename_validate(filename, capsys, hook):
    result = hook.validate(filename)

    output, _ = capsys.readouterr()
    assert output.startswith(filename)
    assert "invalid filename" in output
    assert result is False


@pytest.mark.parametrize("filename", [r"invalid\ dir/file.txt", r"tmp/invalid\ dir/file.txt"])
def test_filename_validate_dirname(filename, capsys, hook):
    result = hook.validate(filename)

    output, _ = capsys.readouterr()
    assert output.startswith(filename)
    assert "invalid dirname" in output
    assert result is False


@pytest.mark.parametrize(
    "filename",
    [
        "Dockerfile" ".gitignore",
        "local.env",
        "script_01.py",
        "__init__.py",
        "something_2018-04-11.log",
        "py/do_something.py",
        "css/bootstrap-3.min.css",
        "templates/product-edit.html",
        "templates/listing-edit.htm",
        "js/angular/angular-1.min.js",
        ".multi/level_01/directories-stuff/file.txt",
    ],
)
def test_filename_validate_unmatch(filename, capsys, hook):
    result = hook.validate(filename)

    output, _ = capsys.readouterr()
    assert output == ""
    assert result is True
