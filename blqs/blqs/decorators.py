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
import dataclasses
import inspect
import types
from typing import Any, Callable, Dict, Iterable, Sequence, Set

import gast


@dataclasses.dataclass
class DecoratorSpec:
    """Specification of a decorator.

    Attributes:
        module: The module in which the decorator is defined.
        method: The decorator method, or, the method which is called to produce the decorator.

    Typical use is to register a new decorator which delegates to build or build_with_config.
    Here is an example usage of defining a new decorator.
        ```
        def my_decorator(func):
            @functools.warps(func)
            def wrapper(*arg, **kwargs)):
                # To avoid circular import, we import the module where my_decorator is defined here.
                import your_module as __your_module
                # Pass in the decorator spec.
                blqs_build_config = blqs.BuildConfig(additional_decorator_specs=
                    [blqs.DecoratorSpec(module=__your_module, method=my_decorator)])

                blqs_func = blqs.build_with_config(blqs_build_config)(func)
                program = blqs_func(*arg, **kwargs)
                # Do your separate processing here.
                ...
            return wrapper
        ```
    """

    module: types.ModuleType
    method: Callable


def _remove_decorators(
    decorators: Sequence, module_aliases: Iterable[str], method_aliases: Iterable[str]
) -> Sequence:
    """Removes decorators specified as a `blqs.DecoratorSpec` from the decorator node list.

    This performs a best effort to remove these annotations. It supports the case where the
    the module or functions are aliased. These aliases are obtained from the captured globals.
    Technically there are cases where expressions evaluate to functions, we avoid having to
    execute these at the cost of not supporting these cases.

    For example it handles cases like this where the function is aliased.
        ```
        from blqs import build as my_build
        @my_build
        def f():
            ....
        ```

    If there are other decorators, this will throw an exception as `blqs` does not currently
    support more than a single decorator.

    Args:
        decorators: The list of AST nodes coming from a function type.
        module_aliases: The matching module aliases to remove.
        method_aliases: The matching method names to remove.

    Raises:
        ValueError: If there is a decorator after the blqs build decorator.
    """
    if len(decorators) == 0:
        return decorators

    for d in decorators:
        # @build style decorator.
        if isinstance(d, gast.Name) and d.id in method_aliases:
            break
        # @blqs.build style decorator.
        elif (
            isinstance(d, gast.Attribute)
            and d.attr in method_aliases
            and isinstance(d.value, gast.Name)
            and d.value.id in module_aliases
        ):
            break
        # @build_with_config(config) style decorator.
        elif (
            isinstance(d, gast.Call)
            and isinstance(d.func, gast.Name)
            and d.func.id in method_aliases
        ):
            break
        # @blqs.build_with_config(config) style decorator.
        elif (
            isinstance(d, gast.Call)
            and isinstance(d.func, gast.Attribute)
            and d.func.attr in method_aliases
            and isinstance(d.func.value, gast.Name)
            and d.func.value.id in module_aliases
        ):
            break
        # Technically there are more cases here since a decorator is an expression, and
        # some expressions could evaluate to the above styles.
    else:
        # No matching decorators found.
        return decorators
    if len(decorators) == 1:
        return []
    raise ValueError(
        "If using build or build_with_config decorator, no other decorators can be used "
        "unless they are unwrapped decorators that operate before the build decorator. "
        "Use build(decorator(func)) or decorator(build(func)) instead."
    )


def _compute_module_aliases(match_decorators, variables: Dict[str, Any]) -> Set:
    valid_modules = set(d.module for d in match_decorators)

    get_aliases = lambda predicate: {k for k, v in variables.items() if predicate(v)}

    module_aliases = get_aliases(lambda o: inspect.ismodule(o) and o in valid_modules)
    module_aliases.update(m.__name__ for m in valid_modules)
    return module_aliases


def _compute_method_aliases(match_decorators, variables: Dict[str, Any]) -> Set:
    valid_methods = set(d.method for d in match_decorators)

    get_aliases = lambda predicate: {k for k, v in variables.items() if predicate(v)}

    method_aliases = get_aliases(lambda o: inspect.isfunction(o) and o in valid_methods)
    method_aliases.update(m.__name__ for m in valid_methods)
    return method_aliases
