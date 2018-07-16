import pytest

from hulks.check_django_migrations_filename import DjangoMigrationFilenameHook


@pytest.fixture
def hook():
    return DjangoMigrationFilenameHook()


@pytest.mark.parametrize(
    'filename',
    [
        'core/migrations/0002_auto_20150315_0043.py',
        'clients/migrations/0002_auto_20180315_0043.py',
        'sellers/migrations/0002_auto_20170315_0043.py',
        'houses/migrations/0002_auto_20180315_0043.py',
        'houses/migrations/0003_auto_20190315_0045.py',
        'houses/migrations/0004_auto_20190315_0043.py',
    ]
)
def test_migration_filename_invalid(filename, capsys, hook):
    result = hook.validate(filename)

    output, _ = capsys.readouterr()

    assert filename in output
    assert 'invalid migration filename' in output
    assert result is False


@pytest.mark.parametrize(
    'filename',
    [
        'core/migrations/0002_CreateUserAdmin.py',
        'core/migrations/0003_UpdateUserAdmin.py',
        'core/migrations/0004_RemoveAvatarField.py',
        'core/migrations/0004_RemoveAvatarField.py',
        'houses/migrations/0004_CreateZipCodeField.py',

    ]
)
def test_migration_filename_valid(filename, capsys, hook):
    result = hook.validate(filename)

    assert result is True
