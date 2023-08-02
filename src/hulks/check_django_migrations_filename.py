import re
import sys
from pathlib import Path
from typing import Any, Dict, Final, NoReturn, Optional, Sequence

from hulks.base import BaseHook


class DjangoMigrationFilenameHook(BaseHook):
    MIGRATIONS_DEFAULT_FILES_PATTERN: Final[str] = r".*\d{4}_\w+_\d{8}_\d{4}"
    CAMEL_CASE_PATTERN: Final[str] = r"^\d{4}_([A-Z]|[a-z])+[A-Z]+"

    def validate(self, filename: str, **options: Dict[str, Any]) -> bool:
        filepath = Path(filename)

        if re.match(self.MIGRATIONS_DEFAULT_FILES_PATTERN, filepath.name):
            print("{}: {}".format(filename, "invalid migration filename, default django name detected"))
            return False

        if re.match(self.CAMEL_CASE_PATTERN, filepath.name):
            print("{}: {}".format(filename, "invalid migration filename, camel case detected"))
            return False

        return True


def main(args: Optional[Sequence[str]] = None) -> NoReturn:
    """Checks if django migrations files are named correctly"""
    hook = DjangoMigrationFilenameHook()
    sys.exit(hook.handle(args))


if __name__ == "__main__":
    main(sys.argv[1:])
