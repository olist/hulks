import re
import sys
from pathlib import Path

from hulks.base import BaseHook


class FilenameHook(BaseHook):
    DIRECTORY_PATTERN = r'^[\w\-\.]+$'
    DEFAULT_FILES_PATTERN = r'^[\w\-\.]+$'
    PYTHON_FILES_PATTERN = r'^[\w]+$'
    WEB_FILES_PATTERN = r'^[A-Za-z0-9\-\.]+$'

    def _validate_path(self, pattern, path):
        return re.match(pattern, path) is not None

    def _validate_directory(self, name):
        if name == '':
            return True

        return self._validate_path(self.DIRECTORY_PATTERN, name)

    def _validate_filename(self, suffix, stem):
        pattern = self.DEFAULT_FILES_PATTERN
        if suffix == '.py':
            pattern = self.PYTHON_FILES_PATTERN
        elif suffix in ('.html', '.htm', '.css', '.js'):
            pattern = self.WEB_FILES_PATTERN

        return self._validate_path(pattern, stem)

    def validate(self, filename):
        file_path = Path(filename)

        for parent in file_path.parents:
            if not self._validate_directory(parent.name):
                print('{}: invalid dirname at "{}"'.format(filename, parent.name))
                return False

        if not self._validate_filename(file_path.suffix, file_path.stem):
            print('{}: invalid filename'.format(filename))
            return False

        return True


def main(args=None):
    """Checks if all file and directory names fit your naming convention"""
    hook = FilenameHook()
    return sys.exit(hook.handle(args))


if __name__ == '__main__':
    main(sys.argv[1:])
