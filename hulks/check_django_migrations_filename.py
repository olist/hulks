import re
import sys

from hulks.base import BaseHook


class DjangoMigrationHook(BaseHook):
    MIGRATIONS_FILES_PATTERN = r'.*[0-9]{4}_\w+_[0-9]{8}_[0-9]{4}.py$'

    def validate(self, filename, **options):

        pattern = self.MIGRATIONS_FILES_PATTERN
        if re.match(pattern, filename):
            print(f'{filename}: invalid migration filename')
            return False

        return True


def main(args=None):
    hook = DjangoMigrationHook()
    sys.exit(hook.handle(args))


if __name__ == '__main__':
    main(sys.argv[1:])
