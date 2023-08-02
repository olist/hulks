import re
import sys
from typing import Any, Dict, NoReturn, Optional, Sequence

from hulks.base import BaseHook


class CheckLoggerHook(BaseHook):
    def _show_error_message(self, filename: str, line_number: int) -> None:
        msg = "{}, line={}: preferably logger should be set with __name__"
        print(msg.format(filename, line_number))

    def validate(self, filename: str, **options: Dict[str, Any]) -> bool:
        retval = True
        pattern = re.compile(r"\((.+)\)")
        for lino, line in self.lines_iterator(filename):
            if "getLogger(" not in line:
                continue

            if line.startswith((" ", "\t")):
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
                if mt == "__name__":
                    continue

                self._show_error_message(filename, lino)
                retval = False
                continue

        return retval


def main(args: Optional[Sequence[str]] = None) -> NoReturn:
    """Checks 'getLogger' usage"""
    hook = CheckLoggerHook()
    sys.exit(hook.handle(args))


if __name__ == "__main__":
    main(sys.argv[1:])
