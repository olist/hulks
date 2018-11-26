import argparse
import mimetypes
import sys


class BaseHook:

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
            last_retval = self.validate(filename, **cmd_options)
            retval = last_retval and retval

        return int(not retval)

    def lines_iterator(self, filename):
        if not mimetypes.guess_type(filename)[0].startswith('text/'):
                print(f'[WARNING] Trying to iterate lines of non-text file {filename!r}. '
                      'Double-check commit-hook configuration!', file=sys.stderr)
        try:
            with open(filename) as fp:
                for line_number, line in enumerate(fp.readlines(), 1):
                    # heuristic, so we dont need to handle all "comment" syntax accross languages
                    if ' noqa' not in line.lower():
                        yield line_number, line
        except UnicodeDecodeError as error:
            *args, reason = error.args
            reason += f' at file {filename!r}!'
            raise UnicodeDecodeError(*(args + [reason]))
