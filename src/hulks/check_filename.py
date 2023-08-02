import re
import sys
from pathlib import Path
from typing import Any, Dict, Final, NoReturn, Optional, Sequence

from hulks.base import BaseHook


class FilenameHook(BaseHook):
    DIRECTORY_PATTERN: Final[str] = r"^[\w\-\.]+$"
    DEFAULT_FILES_PATTERN: Final[str] = r"^[\w\-\.]+$"
    PYTHON_FILES_PATTERN: Final[str] = r"^[\w]+$"
    WEB_FILES_PATTERN: Final[str] = r"^[A-Za-z0-9\-\.]+$"

    def _validate_path(self, pattern: str, path: str) -> bool:
        return re.match(pattern, path) is not None

    def _validate_directory(self, name: str) -> bool:
        if name == "":
            return True

        return self._validate_path(self.DIRECTORY_PATTERN, name)

    def _validate_filename(self, suffix: str, stem: str) -> bool:
        pattern = self.DEFAULT_FILES_PATTERN
        if suffix == ".py":
            pattern = self.PYTHON_FILES_PATTERN
        elif suffix in (".html", ".htm", ".css", ".js"):
            pattern = self.WEB_FILES_PATTERN

        return self._validate_path(pattern, stem)

    def validate(self, filename: str, **options: Dict[str, Any]) -> bool:
        file_path = Path(filename)

        for parent in file_path.parents:
            if not self._validate_directory(parent.name):
                print(f'{filename}: invalid dirname at "{parent.name}"')
                return False

        if not self._validate_filename(file_path.suffix, file_path.stem):
            print(f"{filename}: invalid filename")
            return False

        return True


def main(args: Optional[Sequence[str]] = None) -> NoReturn:
    """Checks if all file and directory names fit your naming convention"""
    hook = FilenameHook()
    sys.exit(hook.handle(args))


if __name__ == "__main__":
    main(sys.argv[1:])
