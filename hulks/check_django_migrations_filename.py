import re
import sys
from pathlib import Path

from hulks.base import BaseHook


class DjangoMigrationFilenameHook(BaseHook):
    MIGRATIONS_DEFAULT_FILES_PATTERN = r'.*[0-9]{4}_\w+_[0-9]{8}_[0-9]{4}'
    CAMEL_CASE_PATTERN = r'^[0-9]{4}_[A-Z][a-z0-9]+[A-z][a-z]+'

    def validate(self, filename, **options):
        file = Path(filename)
        valid = True
        pattern = self.MIGRATIONS_DEFAULT_FILES_PATTERN
        camel_case_pattern = self.CAMEL_CASE_PATTERN

        if re.match(pattern, file.name):
            msg = 'invalid migration filename, default django name detected'
            print(f'{filename}: {msg}')
            valid = False

        if re.match(camel_case_pattern, file.name):
            msg = 'invalid migration filename, camel case detected'
            print(f'{filename}: {msg}')
            valid = False
        return valid


def main(args=None):
    hook = DjangoMigrationFilenameHook()
    sys.exit(hook.handle(args))


if __name__ == '__main__':
    main(sys.argv[1:])
