import sys
from typing import Any, Dict, NoReturn, Optional, Sequence

from hulks.base import BaseHook


class ExampleHook(BaseHook):
    def validate(self, filename: str, **options: Dict[str, Any]) -> bool:
        retval = True
        for lino, line in self.lines_iterator(filename):
            if "batman" in line:
                found = "line={}, col={}".format(lino, line.index("batman") + 1)
                print(f"{found}: entrei na feira da fruta...")
                retval = False
                break

        return retval


def main(args: Optional[Sequence[str]] = None) -> NoReturn:
    """Example hulk"""
    hook = ExampleHook()
    sys.exit(hook.handle(args))


if __name__ == "__main__":
    main(sys.argv[1:])
