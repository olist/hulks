from abc import ABC, abstractmethod
from argparse import ArgumentParser
from typing import Any, Dict, Iterator, Optional, Sequence, Tuple


class BaseHook(ABC):
    @abstractmethod
    def validate(self, filename: str, **options: Dict[str, Any]) -> bool:
        pass

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def handle(self, args: Optional[Sequence[str]] = None) -> int:
        parser = ArgumentParser()
        parser.add_argument("filenames", nargs="*", help="Filenames to fix")
        self.add_arguments(parser)

        parsed = parser.parse_args(args)
        options = vars(parsed)
        filenames: Sequence[str] = options.pop("filenames")

        retval = True

        for filename in filenames:
            last_retval = self.validate(filename, **options)
            retval = last_retval and retval

        return int(not retval)

    def lines_iterator(self, filename: str) -> Iterator[Tuple[int, str]]:
        with open(filename) as fp:
            try:
                lines = list(fp)
            except UnicodeDecodeError as error:
                reason = f"{error.reason} at file {filename!r}!"
                raise UnicodeDecodeError(error.encoding, error.object, error.start, error.end, reason)

        for line_number, line in enumerate(lines, 1):
            # heuristic, so we dont need to handle all "comment" syntax accross languages
            if " noqa" not in line.lower():
                yield line_number, line
