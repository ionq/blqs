import ast
import astunparse
import functools
import gast
import inspect
import importlib
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
        # This pattern is used to correctly capture closures.
        transformer = _BuildTransformer(func)
        transformed_ast, outer_fn_name = transformer.transform(root)

        # Convert back to ast and get the code.
        root_ast = gast.gast_to_ast(transformed_ast)
        transformed_source_code = astunparse.unparse(root_ast).strip()

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

        # Replace function with an outer function, along the inner function that
        # builds the appropriate block.
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
        self._outer_fn_name = self._namer.new_name("outer_fn")
        new_fn = _template.replace(
            template,
            outer_fn=self._outer_fn_name,
            var_defs=var_defs,
            inner_fn=self._namer.new_name("inner_fn"),
            return_block=self._namer.new_name("return_block"),
            old_body=node.body,
        )
        # Set the inner args to the args of the original function.
        inner = next(x for x in new_fn[0].body if isinstance(x, gast.FunctionDef))
        inner.args = node.args
        return new_fn

    def remove_blqs_build_annotation(self, decorator_list):
        return [
            d for d in decorator_list if not d.value or d.value.id != "blqs" or d.attr != "build"
        ]

    def visit_If(self, node):
        node = self.generic_visit(node)
        template = """
        import contextlib
        cond = test
        is_readable = blqs.is_readable(cond)
        cond_statement = blqs.If(cond) if is_readable else None
        if is_readable or cond:
            with cond_statement.if_block() if cond_statement else contextlib.nullcontext():
                if_body
        if is_readable or not cond:
            with cond_statement.else_block() if cond_statement else contextlib.nullcontext():
                else_body
        """
        new_node = _template.replace(
            template,
            cond=self._namer.new_name("cond"),
            is_readable=self._namer.new_name("is_readable"),
            cond_statement=self._namer.new_name("cond_statement"),
            test=node.test,
            if_body=node.body,
            else_body=node.orelse if node.orelse else gast.Pass(),
        )
        return new_node

    def visit_For(self, node):
        node = self.generic_visit(node)
        template = """
        import contextlib
        is_iterable = blqs.is_iterable(iter)
        for_statement = blqs.For(iter) if is_iterable else None
        for target in ((iter.loop_vars(),) if is_iterable else iter):
            with for_statement.loop_block() if for_statement else contextlib.nullcontext():
                loop_body
        else:
            with for_statement.else_block() if for_statement else contextlib.nullcontext():
                else_body
        """
        new_node = _template.replace(
            template,
            is_iterable=self._namer.new_name("is_iterable"),
            for_statement=self._namer.new_name("for_statement"),
            target=node.target,
            iter=node.iter,
            loop_body=node.body,
            else_body=node.orelse if node.orelse else gast.Pass(),
        )
        return new_node

    def visit_While(self, node):
        node = self.generic_visit(node)
        template = """
        import contextlib
        is_readable = blqs.is_readable(test)
        while_statement = blqs.While(cond) if is_readable else None
        while test or is_readable:
            with while_statement.loop_block() if while_statement else contextlib.nullcontext():
                loop_body
            if is_readable:
                break
        if not test or is_readable:
            with while_statement.else_block() if while_statement else contextlib.nullcontext():
                else_body
        """
        new_node = _template.replace(
            template,
            is_readable=self._namer.new_name("is_readable"),
            while_statement=self._namer.new_name("while_statement"),
            test=node.test,
            loop_body=node.body,
            else_body=node.orelse if node.orelse else gast.Pass(),
        )
        return new_node

    def visit_Assign(self, node):
        node = self.generic_visit(node)
        template = """
        temp_value = value
        readable_targets = blqs.readable_targets(temp_value)
        if len(readable_targets) == 1:
            readable_targets = readable_targets[0]
        if readable_targets:
            assign = blqs.Assign(target_names, temp_value)
            targets = readable_targets
        else:
            targets = temp_value
        """
        target_names = self._targets_names(node.targets)
        new_node = _template.replace(
            template,
            temp_value=self._namer.new_name("temp_value"),
            value=node.value,
            targets=node.targets,
            is_readable=self._namer.new_name("is_readable"),
            assign=self._namer.new_name("assign"),
            target_names=target_names,
        )
        return new_node

    def _targets_names(self, targets):
        names = []
        for target in targets:
            if isinstance(target, gast.Name):
                names.append(gast.Constant(target.id, None))
            elif isinstance(target, gast.Tuple):
                return self._targets_names(target.elts)
            elif isinstance(target, gast.Tuple):
                return self._targets_names(target.elts)
            else:
                assert False
        return gast.Tuple(names, gast.Load)
