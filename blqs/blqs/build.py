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

from blqs import conditional, loops, _namer, _template


def build(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get source.
        source_code = textwrap.dedent(inspect.getsource(func))

        # Parse it.
        root = gast.parse(source_code)

        # Transform the function a builder.
        # This creates an outer function, which when call returns the transformed function.
        transformer = _BuildTransformer(func)
        transformed_ast, outer_fn_name = transformer.transform(root)
        print(gast.dump(transformed_ast))

        # Convert back to ast and get the code.
        root_ast = gast.gast_to_ast(transformed_ast)
        transformed_source_code = astunparse.unparse(root_ast).strip()
        print(transformed_source_code)

        # Write a temp file with the new source code.
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
        node = self.generic_visit(node)
        if node.name != self._func.__name__:
            return node
        # If this comes from a decorator, remove it.
        node.decorator_list = self.remove_blqs_build_annotation(node.decorator_list)

        # Replace function with an outer function, along with a
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
            old_body=node.body,
        )
        return new_module.body[0]

    def remove_blqs_build_annotation(self, decorator_list):
        return [
            d for d in decorator_list if not d.value or d.value.id != "blqs" or d.attr != "build"
        ]

    def visit_If(self, node):
        node = self.generic_visit(node)

        if node.orelse:
            template = """
            cond = test
            def if_fn():
                if_body
            def else_fn():
                else_body

            if hasattr(cond, 'is_readable'):
                cond_statement = blqs.If(cond)
                with cond_statement.if_block():
                    if_fn()
                with cond_statement.else_block():
                    else_fn()
            else:
                if cond:
                    if_fn()
                else:
                    else_fn()
            """
        else:
            template = """
            cond = test
            def if_fn():
                if_body

            if hasattr(cond, 'is_readable'):
                cond_statement = blqs.If(cond)
                with cond_statement.if_block():
                    if_fn()
            else:
                if cond:
                    if_fn()
            """

        new_node = _template.replace(
            template,
            cond=self._namer.new_name("cond", ()),
            cond_statement=self._namer.new_name("if_statement", ()),
            test=node.test,
            if_body=node.body,
            else_body=node.orelse,
        )
        return new_node

    def visit_For(self, node):
        node = self.generic_visit(node)

        if node.orelse:
            template = """
            def loop_fn():
                loop_body
            def else_fn():
                else_body

            if hasattr(iter, 'is_iterable'):
                for_statement = blqs.For(iter)
                target = iter.loop_vars()
                with for_statement.loop_block():
                    loop_fn()
                with for_statement.else_block():
                    else_fn()
            else:
                for target in iter:
                    loop_fn()
                else:
                    else_fn()
            """
        else:
            template = """
            def loop_fn():
                loop_body

            if hasattr(iter, 'is_iterable'):
                for_statement = blqs.For(iter)
                target = iter.loop_vars()
                with for_statement.loop_block():
                    loop_fn()
            else:
                for target in iter:
                    loop_fn()
            """
        new_node = _template.replace(
            template,
            loop_fn=self._namer.new_name("loop_fn", ()),
            for_statement=self._namer.new_name("for_statement", ()),
            target=node.target,
            iter=node.iter,
            loop_body=node.body,
            else_body=node.orelse,
        )
        return new_node

    def visit_While(self, node):
        node = self.generic_visit(node)
        if node.orelse:
            template = """
            def loop_fn():
                loop_body
            def else_fn():
                else_body

            if hasattr(test, 'is_readable'):
                while_statement = blqs.While(cond)
                with while_statement.loop_block():
                    loop_fn()
                with while_statement.else_block():
                    else_fn()
            else:
                while(test):
                    loop_fn()
                else:
                    else_fn()
            """
        else:
            template = """
            def loop_fn():
                loop_body

            if hasattr(test, 'is_readable'):
                while_statement = blqs.While(cond)
                with while_statement.loop_block():
                    loop_fn()
            else:
                while(test):
                    loop_fn()
            """
        new_node = _template.replace(
            template,
            loop_fn=self._namer.new_name("loop_fn", ()),
            while_statement=self._namer.new_name("while_statement", ()),
            test=node.test,
            loop_body=node.body,
            else_body=node.orelse,
        )
        return new_node