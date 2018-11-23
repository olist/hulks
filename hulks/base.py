import argparse
import mimetypes


class BaseHook:

    CHECK_BINARY_FILES = True

    def validate(self, filename, **options):
        raise NotImplementedError()

    def add_arguments(self, parser):
        pass

    def handle(self, args=None):
        parser = argparse.ArgumentParser()
        parser.add_argument('filenames', nargs='*', help='Filenames to fix')
        self.add_arguments(parser)
        args = parser.parse_args(args)
        options = vars(args)
        cmd_options = {k: options[k] for k in options if k != 'filenames'}

        retval = True

        for filename in args.filenames:
            if not self.CHECK_BINARY_FILES and \
                    not mimetypes.guess_type(filename)[0].startswith('text/'):
                continue
            last_retval = self.validate(filename, **cmd_options)
            retval = last_retval and retval

        return int(not retval)

    def lines_iterator(self, filename):
        with open(filename) as fp:
            for line_number, line in enumerate(fp.readlines(), 1):
                # heuristic, so we dont need to handle all "comment" syntax accross languages
                if ' noqa' not in line.lower():
                    yield line_number, line
