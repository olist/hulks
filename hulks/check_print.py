import ast
import sys

from hulks.base import BaseHook


class CheckPrintHook(BaseHook):
    def _show_error_message(self, filename, line_number):
        msg = "{}, line={}: call to print found, please remove it."
        print(msg.format(filename, line_number))

    def validate(self, filename, **options):
        retval = True
        parsed_tree = ast.parse(open(filename).read(), filename)
        for node in ast.walk(parsed_tree):
            if isinstance(node, ast.Name) and node.id == "print":
                self._show_error_message(filename, node.lineno)
                retval = False
        return retval


def main(args=None):
    """Checks 'print' usage"""
    hook = CheckPrintHook()
    sys.exit(hook.handle(args))


if __name__ == "__main__":
    main(sys.argv[1:])
