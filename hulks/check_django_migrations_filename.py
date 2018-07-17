import re
import sys
from pathlib import Path

from hulks.base import BaseHook


class DjangoMigrationFilenameHook(BaseHook):
    MIGRATIONS_DEFAULT_FILES_PATTERN = r'.*\d{4}_\w+_\d{8}_\d{4}'
    CAMEL_CASE_PATTERN = r'^\d{4}_[A-Z][a-z0-9]+[A-z][a-z]+'

    def validate(self, filename, **options):
        filepath = Path(filename)
        valid = True

        if re.match(self.MIGRATIONS_DEFAULT_FILES_PATTERN, filepath.name):
            msg = 'invalid migration filename, default django name detected'
            print(f'{filename}: {msg}')
            valid = False

        if re.match(self.CAMEL_CASE_PATTERN, filepath.name):
            msg = 'invalid migration filename, camel case detected'
            print(f'{filename}: {msg}')
            valid = False

        return valid


def main(args=None):
    hook = DjangoMigrationFilenameHook()
    sys.exit(hook.handle(args))


if __name__ == '__main__':
    main(sys.argv[1:])
