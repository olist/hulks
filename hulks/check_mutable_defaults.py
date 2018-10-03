import ast
import sys

from hulks.base import BaseHook


class CheckMutableDefaults(BaseHook):
    _immutable_builtins = ('bool', 'int', 'float', 'tuple', 'str', 'frozenset', 'object')
    _ast_mutable_types = (
        ast.List,
        ast.Set,
        ast.Dict,
    )

    def _collect_functions_with_defaults(self, tree):
        nodes = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef):
                continue

            if node.args and node.args.defaults:
                nodes.append(node)

        return nodes

    def _check_mutable_defaults(self, filename, node):
        retval = True
        for default_arg_value in node.args.defaults:
            conditions = (
                isinstance(default_arg_value, self._ast_mutable_types),
                isinstance(default_arg_value, ast.Call) and
                default_arg_value.func.id not in self._immutable_builtins,
            )
            if any(conditions):
                msg = 'mutable default found: {}:{}:{} ({})'
                print(msg.format(filename, node.lineno, default_arg_value.col_offset, node.name))
                retval = False

        return retval

    def validate(self, filename, **options):
        retval = True
        parsed = ast.parse(open(filename).read(), filename)
        fn_nodes = self._collect_functions_with_defaults(parsed)
        for node in fn_nodes:
            retval = self._check_mutable_defaults(filename, node)

        return retval


def main(args=None):
    """Check mutable defaults arguments in python code"""
    hook = CheckMutableDefaults()
    sys.exit(hook.handle(args))


if __name__ == '__main__':
    main(sys.argv[1:])
