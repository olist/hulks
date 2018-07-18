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
def test_migration_filename_default_invalid(filename, capsys, hook):
    result = hook.validate(filename)
    output, _ = capsys.readouterr()

    assert filename in output
    assert 'default django name detected' in output
    assert result is False


@pytest.mark.parametrize(
    'filename',
    [
        'core/migrations/0002_CreateUserAdmin.py',
        'core/migrations/0003_UpdateUserAdmin.py',
        'core/migrations/0004_RemoveAvatarField.py',
        'core/migrations/0004_RemoveAvatarPicture.py',
        'houses/migrations/0004_createZipCodeField.py',
        'houses/migrations/0005_lowerCamelCase.py',
    ]
)
def test_migration_filename_camel_case_invalid(filename, capsys, hook):
    result = hook.validate(filename)
    output, _ = capsys.readouterr()

    assert filename in output
    assert 'camel case detected' in output
    assert result is False


@pytest.mark.parametrize(
    'filename',
    [
        'core/migrations/0002_create_user_admin.py',
        'core/migrations/0003_update_user_admin.py',
        'core/migrations/0004_remove_avatar_field.py',
        'core/migrations/0004_remove_avatar_picture.py',
        'houses/migrations/0004_create_zip_code_field.py',
    ]
)
def test_migration_filename_valid(filename, capsys, hook):
    result = hook.validate(filename)

    assert result is True
