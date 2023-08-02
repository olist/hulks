import ast
import sys
from typing import Any, Dict, Iterable, List, NoReturn, Optional, Sequence, Union, cast

from hulks.base import BaseHook

_immutable_builtins = ("bool", "float", "frozenset", "int", "object", "str", "tuple")
_ast_mutable_types = (ast.List, ast.Set, ast.Dict)
_assigns = (ast.AnnAssign, ast.Assign)


class CheckMutableDefaults(BaseHook):
    def _collect_functions_with_defaults(
        self, tree: ast.Module
    ) -> Iterable[Union[ast.FunctionDef, ast.AsyncFunctionDef]]:
        nodes: List[Union[ast.FunctionDef, ast.AsyncFunctionDef]] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            if node.args and node.args.defaults:
                nodes.append(node)

        return nodes

    def _collect_class_attributes(self, tree: ast.Module) -> Iterable[ast.AST]:
        nodes = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue

            nodes += [cls_node for cls_node in node.body if isinstance(cls_node, _assigns)]

        return nodes

    def _check_mutable_value(self, value: Optional[ast.AST]) -> bool:
        if isinstance(value, ast.Tuple) and any(self._check_mutable_value(elt) for elt in value.elts):
            return True

        if isinstance(value, _ast_mutable_types):
            return True

        if isinstance(value, ast.Call) and isinstance(value.func, ast.Name):
            return value.func.id not in _immutable_builtins

        return False

    def _check_function_node_mutability(
        self, filename: str, node: Union[ast.FunctionDef, ast.AsyncFunctionDef]
    ) -> bool:
        retval = True
        for default_arg_value in node.args.defaults:
            if self._check_mutable_value(default_arg_value):
                msg = "mutable default found: {}:{}:{} ({})"
                print(msg.format(filename, node.lineno, default_arg_value.col_offset, node.name))
                retval = False

        return retval

    def _check_functions(self, parsed: ast.Module, filename: str) -> bool:
        fn_nodes = self._collect_functions_with_defaults(parsed)
        return all(self._check_function_node_mutability(filename, node) for node in fn_nodes)

    def _check_assign_node_mutability(self, filename: str, node: Union[ast.AnnAssign, ast.Assign]) -> bool:
        if not self._check_mutable_value(node.value):
            return True

        if not self.strict:
            return True

        target = node.targets[0] if isinstance(node, ast.Assign) else node.target
        name = cast(ast.Name, target).id

        if isinstance(name, bytes):
            name = name.decode()

        if name.isupper() or name.startswith("_"):
            return True

        msg = "mutable default found: {}:{}:{} ({})"
        print(msg.format(filename, node.lineno, node.col_offset, name))
        return False

    def _check_classes(self, parsed: ast.Module, filename: str) -> bool:
        cls_nodes = self._collect_class_attributes(parsed)
        return all(
            self._check_assign_node_mutability(filename, node)
            for node in cls_nodes
            if isinstance(node, _assigns)
        )

    def validate(self, filename: str, **options: Dict[str, Any]) -> bool:
        self.strict = options.get("strict", False)
        parsed = ast.parse(open(filename).read(), filename)
        return self._check_classes(parsed, filename) and self._check_functions(parsed, filename)


def main(args: Optional[Sequence[str]] = None) -> NoReturn:
    """Check mutable defaults arguments in python code"""
    hook = CheckMutableDefaults()
    sys.exit(hook.handle(args))


if __name__ == "__main__":
    main(sys.argv[1:])
