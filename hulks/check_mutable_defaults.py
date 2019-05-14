import ast
import sys

from hulks.base import BaseHook


class CheckMutableDefaults(BaseHook):
    _immutable_builtins = ("bool", "float", "frozenset", "int", "object", "str", "tuple")
    _ast_mutable_types = (ast.List, ast.Set, ast.Dict)

    def _collect_functions_with_defaults(self, tree):
        nodes = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            if node.args and node.args.defaults:
                nodes.append(node)

        return nodes

    def _collect_class_attributes(self, tree):
        nodes = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            nodes += [cls_node for cls_node in node.body if isinstance(cls_node, (ast.AnnAssign, ast.Assign))]

        return nodes

    def _check_mutable_value(self, value):
        if isinstance(value, ast.Tuple) and any(self._check_mutable_value(elt) for elt in value.elts):
            return True

        if isinstance(value, self._ast_mutable_types):
            return True

        try:
            return value.func.id not in self._immutable_builtins
        except AttributeError as exc:
            if isinstance(value, ast.Call) and not isinstance(value.func, ast.Attribute):
                raise exc

        return False

    def _check_function_node_mutability(self, filename, node):
        retval = True
        for default_arg_value in node.args.defaults:
            if self._check_mutable_value(default_arg_value):
                msg = "mutable default found: {}:{}:{} ({})"
                print(msg.format(filename, node.lineno, default_arg_value.col_offset, node.name))
                retval = False

        return retval

    def _check_functions(self, parsed, filename):
        fn_nodes = self._collect_functions_with_defaults(parsed)
        return all(self._check_function_node_mutability(filename, node) for node in fn_nodes)

    def _check_assign_node_mutability(self, filename, node):
        if not self._check_mutable_value(node.value):
            return True

        if not self.strict:
            return True

        try:
            name = node.targets[0].id
        except AttributeError:
            name = node.target.id

        if isinstance(name, bytes):
            name = name.decode()

        if name.isupper() or name.startswith("_"):
            return True

        msg = "mutable default found: {}:{}:{} ({})"
        print(msg.format(filename, node.lineno, node.col_offset, name))
        return False

    def _check_classes(self, parsed, filename):
        cls_nodes = self._collect_class_attributes(parsed)
        return all(self._check_assign_node_mutability(filename, node) for node in cls_nodes)

    def validate(self, filename, **options):
        self.strict = options.get("strict", False)
        parsed = ast.parse(open(filename).read(), filename)
        return self._check_classes(parsed, filename) and self._check_functions(parsed, filename)


def main(args=None):
    """Check mutable defaults arguments in python code"""
    hook = CheckMutableDefaults()
    sys.exit(hook.handle(args))


if __name__ == "__main__":
    main(sys.argv[1:])
