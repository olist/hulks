import ast
import sys

from hulks.base import BaseHook


class CheckMutableDefaults(BaseHook):
    _immutable_builtins = (
        'bool',
        'float',
        'frozenset',
        'int',
        'object',
        'str',
        'tuple',
    )
    _ast_mutable_types = (
        ast.List,
        ast.Set,
        ast.Dict,
    )

    def _collect_functions_with_defaults(self, tree):
        nodes = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            if node.args and node.args.defaults:
                nodes.append(node)

        return nodes

    def _check_mutable_value(self, value):
        retval = False
        if isinstance(value, ast.Tuple):
            retval = any(self._check_mutable_value(elt) for elt in value.elts)

        conditions = (
            retval,
            isinstance(value, self._ast_mutable_types),
            isinstance(value, ast.Call) and value.func.id not in self._immutable_builtins,
        )
        return any(conditions)

    def _check_node_mutability(self, filename, node):
        retval = True
        for default_arg_value in node.args.defaults:
            if self._check_mutable_value(default_arg_value):
                msg = 'mutable default found: {}:{}:{} ({})'
                print(msg.format(filename, node.lineno, default_arg_value.col_offset, node.name))
                retval = False

        return retval

    def validate(self, filename, **options):
        parsed = ast.parse(open(filename).read(), filename)
        fn_nodes = self._collect_functions_with_defaults(parsed)
        return all(self._check_node_mutability(filename, node) for node in fn_nodes)


def main(args=None):
    """Check mutable defaults arguments in python code"""
    hook = CheckMutableDefaults()
    sys.exit(hook.handle(args))


if __name__ == '__main__':
    main(sys.argv[1:])
