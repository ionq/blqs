import ast
import astunparse
import functools
import gast
import importlib
import inspect
import imp
import os
import sys
import textwrap
import types
import tempfile

from blqs import conditional, _namer, _template


def build(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get source.
        source_code = textwrap.dedent(inspect.getsource(func))

        # Parse it.
        root = gast.parse(source_code)

        # Do the transform.
        transformer = _BuildTransformer(func)
        transformed_ast, outer_fn_name = transformer.transform(root)

        # Convert back to ast and get the code.
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

        # Get the outer function, and call it, returning the inner function.
        new_func = getattr(module, outer_fn_name)()  # pylint: disable=not-callable
        # Set this inner function up with the correct globals and closure.
        final_func = types.FunctionType(
            code=new_func.__code__, globals=func.__globals__, closure=func.__closure__
        )
        return final_func(*args, **kwargs)  # pylint: disable=not-callable

    return wrapper


class _BuildTransformer(gast.NodeTransformer):
    def __init__(self, func):
        self._func = func
        self._local_vars = func.__code__.co_freevars + func.__code__.co_varnames
        self._namer = _namer.Namer(func.__globals__.keys())
        self._outer_fn_name = None

    def transform(self, node):
        transformed_node = self.visit(node)
        assert self._outer_fn_name is not None
        return transformed_node, self._outer_fn_name

    def visit_FunctionDef(self, node):
        if node.name != self._func.__name__:
            return node
        # If this comes from a decorator, remove it.
        node.decorator_list = self.remove_blqs_build_annotation(node.decorator_list)

        # Visit function body.
        old_body = self.generic_visit(node).body

        template = """
        def outer_fn():
            var_defs
            def inner_fn():
                with blqs.Block() if blqs.get_current_block() else blqs.Program() as return_block:
                    old_body
                return return_block
            return inner_fn
        """
        var_defs = [
            _template.replace(f"var_name = None", var_name=var)
            for var in self._func.__code__.co_freevars
        ]
        self._outer_fn_name = self._namer.new_name("outer_fn", ())
        new_module = _template.replace(
            template,
            outer_fn=self._outer_fn_name,
            var_defs=var_defs,
            inner_fn=self._namer.new_name("inner_fn", ()),
            return_block=self._namer.new_name("return_block", ()),
            old_body=old_body,
        )
        return new_module.body[0]

    def remove_blqs_build_annotation(self, decorator_list):
        return [
            d for d in decorator_list if not d.value or d.value.id != "blqs" or d.attr != "build"
        ]

    def visit_If(self, node):
        template = (
            "cond = test\n"
            "cond_statement = blqs.If(cond) if hasattr(cond, 'has_value') else blqs.BareIf(cond)\n"
            "if cond_statement.if_block():\n"
            "    with cond_statement.if_block():\n"
            "        if_body\n"
            "if cond_statement.else_block():\n"
            "    with cond_statement.else_block():\n"
            "        else_body\n"
        )
        new_body = _template.replace(
            template,
            cond=self._namer.new_name("cond", ()),
            cond_statement=self._namer.new_name("if_statement", ()),
            test=node.test,
            if_body=node.body,
            else_body=node.orelse,
        )
        return new_body
