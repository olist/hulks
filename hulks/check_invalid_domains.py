import sys

from hulks.base import BaseHook


class InvalidDomainsHook(BaseHook):
    INVALID_DOMAINS = [".herokuapp.com"]

    def validate(self, filename):
        result = True
        for i, line in self.lines_iterator(filename):
            for invalid_domain in self.INVALID_DOMAINS:
                if invalid_domain in line:
                    print(
                        '{}: found "{}" line={}, column={}'.format(
                            filename, invalid_domain, i, line.index(invalid_domain) + 1
                        )
                    )
                    result = False

        return result


def main(args=None):
    """Checks file content for invalid domains"""
    hook = InvalidDomainsHook()
    sys.exit(hook.handle(args))


if __name__ == "__main__":
    main(sys.argv[1:])
