# Copyright 2021 The Blqs Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import collections
import dataclasses
import functools
import inspect
import importlib
import os
import sys
import textwrap
import types
import tempfile

from typing import Callable, Optional, Sequence
import astunparse
import gast

from blqs import decorators, exceptions, _ast, _namer, _template


@dataclasses.dataclass
class BuildConfig:
    """Configuration for the build compilation.

    Attributes:
        support_if: Whether to support capturing `if` statements.
        support_for: Whether to support capturing `for` statements.
        support_while: Whether to support capturing `while` statements.
        support_assign: Whether to support capturing assignments.
        support_delete: Whether to support capturing `del` statements.
        additional_decorator_specs: A list of `blqs.DecoratorSpec`s that are removed
            during the build. See `blqs.DecoratorSpec` for more information.
    """

    support_if: bool = True
    support_for: bool = True
    support_while: bool = True
    support_assign: bool = True
    support_delete: bool = True

    additional_decorator_specs: Sequence[decorators.DecoratorSpec] = ()


def build(func: Callable):
    """Turn the supplied function into a builder for the code the function contains.

    Typical use is as decorator:
        ```
        @build
        def my_func(my_arg):
            my_code

        built_func = my_func(a_arg)
        ```
    but can also be called directly:
        ```
        def my_func(my_arg):
            my_code

        build_func = build(my_func)(a_arg)
        ```

    If one wants to pass in a configuration for the build stage, see `build_with_config`.
    """
    return _build(func)


def build_with_config(build_config: BuildConfig) -> Callable:
    """A factory for producing a `blqs.build` decorator with the given configuration.

    Typical use is in creating a decorator with the given config
        ```
        @build_with_config(build_config=my_config)
        def my_func(my_arg):
            my_code

        built_func = my_func(a_arg)
        ```
    """
    return functools.partial(_build, build_config=build_config)


def _build(func: Callable, build_config: Optional[BuildConfig] = None) -> Callable:
    """Turn the supplied function into a builder for the code the function contains.

    This method is not intended to be called directly, use build or build_with_config above.
    """
    # The AST rewrite (parse, transform, write tempfile, import as module, build
    # final_func) is expensive but only depends on `func` and `build_config`, so
    # it's done once on the first call and cached. Doing it lazily — rather than
    # at decoration time — keeps any rewrite errors at call time, which some
    # callers rely on (e.g. functions stacked with another decorator on top of
    # `@blqs.build` raise `ValueError` on call, not at import).
    cache: dict = {}

    def _ensure_built():
        if cache:
            return
        # Get source.
        source_code = textwrap.dedent(inspect.getsource(func))

        # Parse it.
        root = gast.parse(source_code)

        # Transform the function via the transform below.
        # This creates an outer function, which when call returns the transformed function.
        # This pattern is used to correctly capture closures.
        transformer = _BuildTransformer(func, build_config or BuildConfig())
        transformed_gast, outer_fn_name = transformer.transform(root)

        # Convert back to ast and get the code, preserving annotations.
        transformed_ast = _ast.gast_to_ast(transformed_gast)
        transformed_source_code = astunparse.unparse(transformed_ast).strip()

        # Write a temp file with the new source code.
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False, encoding="utf-8"
        ) as f:
            module_name = os.path.basename(f.name[:-3])
            filename = f.name
            f.write(transformed_source_code)

        # Import this new code into the temp module.
        spec = importlib.util.spec_from_file_location(module_name, filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module

        # Get the outer function, and call it, returning the inner function.
        new_func = getattr(module, outer_fn_name)()  # pylint: disable=not-callable
        # Set this inner function up with the correct globals and closure.
        cache["final_func"] = types.FunctionType(
            code=new_func.__code__, globals=func.__globals__, closure=func.__closure__
        )
        # Defer line-map construction: it's only needed on exceptions, and
        # `construct_line_map` has a known assertion that can fire on otherwise
        # well-formed rewrites (preserved as-is from the original behavior, which
        # only constructed it inside the exception handler).
        cache["transformed_gast"] = transformed_gast
        cache["transformed_source_code"] = transformed_source_code
        cache["filename"] = filename

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _ensure_built()
        try:
            return cache["final_func"](*args, **kwargs)  # pylint: disable=not-callable
        except Exception as e:
            # If there is an exception, chain the exception in such a way as to indicated
            # the original file and line number is given.
            if "line_map" not in cache:
                cache["line_map"] = _ast.construct_line_map(
                    cache["transformed_gast"], cache["transformed_source_code"]
                )
            exceptions._raise_with_line_mapping(e, func, cache["line_map"], cache["filename"])

    return wrapper


class _BuildTransformer(gast.NodeTransformer):
    def __init__(self, func: types.FunctionType, build_config: BuildConfig):
        self._func = func
        self._build_config = build_config
        self._local_vars = func.__code__.co_freevars + func.__code__.co_varnames
        self._namer = _namer.Namer(tuple(func.__globals__.keys()))
        self._outer_fn_name = None

    def transform(self, node):
        transformed_node = self.visit(node)
        assert self._outer_fn_name is not None
        return transformed_node, self._outer_fn_name

    def visit(self, node):
        new_nodes = super().visit(node)
        return self._annotate_nodes(node, new_nodes)

    def _annotate_nodes(self, original, new_nodes):
        if hasattr(original, "lineno"):
            if isinstance(new_nodes, collections.abc.Iterable):
                for new_node in new_nodes:
                    new_node.original_lineno = original.lineno
            else:
                new_nodes.original_lineno = original.lineno
        return new_nodes

    def visit_FunctionDef(self, node):
        node = self.generic_visit(node)
        if node.name != self._func.__name__:
            return node
        # If this comes from a decorator, remove it.
        new_decorator_list = self.remove_blqs_build_annotations(node.decorator_list)
        # Replace function with an outer function, along the inner function that
        # builds the appropriate block.
        template = """
        def outer_fn():
            var_defs

            def inner_fn():
                import blqs
                import contextlib
                with blqs.Block() if blqs.get_current_block() else blqs.Program() as return_block:
                    old_body
                return return_block
            return inner_fn
        """
        var_defs = [
            _template.replace("var_name = None", var_name=var)
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
        # Set the inner args to the args of the original function and similarly for decorators.
        inner = next(x for x in new_fn[0].body if isinstance(x, gast.FunctionDef))
        inner.args = node.args
        inner.decorator_list = new_decorator_list
        return new_fn

    def remove_blqs_build_annotations(self, decorator_list: Sequence):
        """Removes any"""
        import blqs as __blqs

        decorator_specs = [
            decorators.DecoratorSpec(module=__blqs, method=build),
            decorators.DecoratorSpec(module=__blqs, method=build_with_config),
            *self._build_config.additional_decorator_specs,
        ]
        module_aliases = decorators._compute_module_aliases(decorator_specs, self._func.__globals__)
        method_aliases = decorators._compute_method_aliases(decorator_specs, self._func.__globals__)

        return decorators._remove_decorators(
            decorator_list, module_aliases=module_aliases, method_aliases=method_aliases
        )

    def visit_If(self, node):
        node = self.generic_visit(node)
        if not self._build_config.support_if:
            return node
        template = """
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
        new_nodes = _template.replace(
            template,
            cond=self._namer.new_name("cond"),
            is_readable=self._namer.new_name("is_readable"),
            cond_statement=self._namer.new_name("cond_statement"),
            test=node.test,
            if_body=node.body,
            else_body=node.orelse if node.orelse else gast.Pass(),
        )
        return new_nodes

    def visit_For(self, node):
        node = self.generic_visit(node)
        if not self._build_config.support_for:
            return node

        # Bind the iterable expression to a local once. The original code re-evaluated
        # `iter` for the is_iterable / For() / loop_vars() / for-loop slots, which
        # double-runs side effects (e.g. on generators or open()).
        template = """
        iter_value = iter
        is_iterable = blqs.is_iterable(iter_value)
        for_statement = blqs.For(iter_value) if is_iterable else None
        loop_vars = blqs.loop_vars(iter_value) if is_iterable else None
        for target in ([loop_vars if len(loop_vars) > 1 else loop_vars[0]]
                       if is_iterable else iter_value):
            with for_statement.loop_block() if for_statement else contextlib.nullcontext():
                loop_body
        else:
            with for_statement.else_block() if for_statement else contextlib.nullcontext():
                else_body
        """
        new_nodes = _template.replace(
            template,
            iter_value=self._namer.new_name("iter_value"),
            is_iterable=self._namer.new_name("is_iterable"),
            for_statement=self._namer.new_name("for_statement"),
            loop_vars=self._namer.new_name("loop_vars"),
            target=node.target,
            iter=node.iter,
            loop_body=node.body,
            else_body=node.orelse if node.orelse else gast.Pass(),
        )
        return new_nodes

    def visit_While(self, node):
        node = self.generic_visit(node)
        if not self._build_config.support_while:
            return node

        # Track the loop's exit reason with a flag instead of re-evaluating `test`
        # after the loop. The original `if not test or is_readable` re-ran the test
        # expression, doubling side effects for non-trivial conditions.
        template = """
        is_readable = blqs.is_readable(test)
        while_statement = blqs.While(test) if is_readable else None
        loop_exited_normally = False
        while test or is_readable:
            with while_statement.loop_block() if while_statement else contextlib.nullcontext():
                loop_body
            if is_readable:
                break
        else:
            loop_exited_normally = True
        if loop_exited_normally or is_readable:
            with while_statement.else_block() if while_statement else contextlib.nullcontext():
                else_body
        """
        new_nodes = _template.replace(
            template,
            is_readable=self._namer.new_name("is_readable"),
            while_statement=self._namer.new_name("while_statement"),
            loop_exited_normally=self._namer.new_name("loop_exited_normally"),
            test=node.test,
            loop_body=node.body,
            else_body=node.orelse if node.orelse else gast.Pass(),
        )
        return new_nodes

    def visit_Assign(self, node):
        node = self.generic_visit(node)
        if not self._build_config.support_assign:
            return node

        target_names = self._target_names(node.targets)
        if target_names is None:
            # Targets include non-Name expressions (e.g. `obj.x = ...`); leave
            # this assignment alone so native Python semantics apply.
            return node

        template = """
        temp_value = value
        readable_targets = blqs.readable_targets(temp_value)
        if len(readable_targets) == 1:
            readable_targets = readable_targets[0]
        if readable_targets:
            blqs.Assign(assign_names, temp_value)
            targets = readable_targets
        else:
            targets = temp_value
        """
        new_nodes = _template.replace(
            template,
            temp_value=self._namer.new_name("temp_value"),
            value=node.value,
            targets=node.targets,
            readable_targets=self._namer.new_name("readable_targets"),
            assign_names=target_names,
        )
        return new_nodes

    def _target_names(self, targets):
        """Return a `gast.Tuple` of name Constants for `targets`, or None.

        Returns None when any target is something other than a `Name` (or a
        `Tuple`/`List` of `Name`s) — e.g. `obj.x` or `arr[0]`. Callers should
        skip the rewrite in that case so native Python semantics apply.
        """
        names = []
        for target in targets:
            if isinstance(target, gast.Name):
                names.append(gast.Constant(target.id, None))
            elif isinstance(target, (gast.Tuple, gast.List)):
                for t in target.elts:
                    if not isinstance(t, gast.Name):
                        return None
                    names.append(gast.Constant(t.id, None))
            else:
                return None
        return gast.Tuple(names, gast.Load())

    def _flat_targets(self, targets):
        """Flatten Tuple/List targets to a single list of Name nodes.

        Pre: `_target_names(targets)` returned non-None, so every leaf is a Name.
        """
        flat = []
        for target in targets:
            if isinstance(target, gast.Name):
                flat.append(target)
            elif isinstance(target, (gast.Tuple, gast.List)):
                flat.extend(target.elts)
        return flat

    def visit_Delete(self, node):
        node = self.generic_visit(node)
        if not self._build_config.support_delete:
            return node

        target_names = self._target_names(node.targets)
        if target_names is None:
            # Non-Name targets (e.g. `del obj.x`); leave alone for native semantics.
            return node

        flat_targets = self._flat_targets(node.targets)
        target_tuple = gast.Tuple(flat_targets, gast.Load())
        target_values_name = self._namer.new_name("target_values")

        # Capture the live values of all targets first; the per-target conditional
        # native `del` below may unbind some of them, after which referencing the
        # original names would fail with NameError. We need them later for the
        # is_deletable filter that builds the captured `Delete(...)` statement.
        new_nodes = list(
            _template.replace(
                "target_values = target_tuple",
                target_values=target_values_name,
                target_tuple=target_tuple,
            )
        )

        # Per-target conditional native `del` for non-deletable values. The
        # original code emitted `del standard_targets`, which deleted the helper
        # tuple instead of the user's bindings — so `del a` (where `a` is a
        # plain int) didn't actually unbind `a`.
        for target in flat_targets:
            check_template = """
            if not blqs.is_deletable(target):
                del target
            """
            new_nodes.extend(_template.replace(check_template, target=target))

        delete_template = """
        deletable_names = tuple(name for val, name in zip(target_values, target_names)
                                if blqs.is_deletable(val))
        if len(deletable_names) > 0:
            blqs.Delete(deletable_names)
        """
        new_nodes.extend(
            _template.replace(
                delete_template,
                target_values=target_values_name,
                deletable_names=self._namer.new_name("deletable_names"),
                target_names=target_names,
            )
        )
        return new_nodes
