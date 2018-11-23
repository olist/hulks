import sys

from hulks.base import BaseHook


class ExampleHook(BaseHook):

    CHECK_BINARY_FILES = False

    def validate(self, filename, **options):
        retval = True
        for lino, line in self.lines_iterator(filename):
            if 'batman' in line:
                found = 'line={}, col={}'.format(lino, line.index('batman') + 1)
                print('{}: entrei na feira da fruta...'.format(found))
                retval = False
                break

        return retval


def main(args=None):
    """Example hulk"""
    hook = ExampleHook()
    sys.exit(hook.handle(args))


if __name__ == '__main__':
    main(sys.argv[1:])
