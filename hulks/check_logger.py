import re
import sys

from hulks.base import BaseHook


class CheckLoggerHook(BaseHook):

    CHECK_BINARY_FILES = False

    def _show_error_message(self, filename, line_number):
        msg = '{}, line={}: preferably logger should be set with __name__'
        print(msg.format(filename, line_number))

    def validate(self, filename, **options):
        retval = True
        pattern = re.compile('\((.+)\)')
        for lino, line in self.lines_iterator(filename):
            if 'getLogger(' not in line:
                continue

            if line.startswith((' ', '\t')):
                continue

            matcher = re.search(pattern, line)
            if not matcher:
                self._show_error_message(filename, lino)
                retval = False
                continue

            matches = matcher.groups()
            for mt in matches:
                if mt.startswith("'") or mt.startswith('"'):
                    continue
                if mt == '__name__':
                    continue

                self._show_error_message(filename, lino)
                retval = False
                continue

        return retval


def main(args=None):
    """Checks 'getLogger' usage"""
    hook = CheckLoggerHook()
    sys.exit(hook.handle(args))


if __name__ == '__main__':
    main(sys.argv[1:])
