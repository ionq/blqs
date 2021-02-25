import ast
import astunparse
import functools
import gast
import importlib
import inspect
import imp
import os
import sys
import types
import tempfile

from blqs import conditional, _template


def build(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get source
        source_code = inspect.getsource(func)

        # Parse it
        root = gast.parse(source_code)

        # Do the transform.
        transformer = Build(func.__name__)
        transformed_ast = transformer.visit(root)

        # Convert back to ast and get the code
        root_ast = gast.gast_to_ast(transformed_ast)
        transformed_source_code = astunparse.unparse(root_ast).strip()

        # Write a temp file with the new source code.
        # TODO: do we need to clean up?
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            module_name = os.path.basename(f.name[:-3])
            file_name = f.name
            f.write(transformed_source_code)

        # Import this new code into the temp module.
        spec = importlib.util.spec_from_file_location(module_name, file_name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module

        # TODO: we need to capture the closure correctly.
        # I think the problem is that this wrapper executes on definition of the function,
        # we really need to capture closure and globals when function is called?

        # Define a function with the same globals as the original function.
        new_func = types.FunctionType(
            code=getattr(module, func.__name__).__code__, globals=func.__globals__
        )

        return new_func(*args, **kwargs)  # pylint: disable=not-callable

    return wrapper


class Build(gast.NodeTransformer):
    def __init__(self, func_name):
        self._func_name = func_name

    # Replace the annotation and for the function with the annotation, wrap a block and return it.
    def visit_FunctionDef(self, node):
        if node.name == self._func_name:
            new_decorators = []
            for attribute in node.decorator_list:
                if attribute.value and attribute.value.id == "blqs" and attribute.attr == "build":
                    continue
                new_decorators.append(attribute)
            template = (
                "with blqs.Block() as __return_block:\n"
                "    placeholder\n"
                "return __return_block\n"
            )

            old_body = self.generic_visit(node).body

            new_body = _template.replace(template, placeholder=old_body)
            node.body = new_body

        node.decorator_list = new_decorators
        return node

    def visit_If(self, node):
        template = (
            "if hasattr(test, 'has_value'):\n"
            "    __if = blqs.If(test)\n"
            "    with __if.if_block():\n"
            "        if_body\n"
            "    with __if.else_block():\n"
            "        else_body\n"
            "else:\n"
            "    if test:\n"
            "        if_body\n"
            "    else:\n"
            "        else_body\n"
        )
        new_body = _template.replace(
            template, test=node.test, if_body=node.body, else_body=node.orelse
        )
        return new_body
