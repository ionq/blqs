import ast
import astunparse
import inspect
import traceback

import gast

from blqs import _ast, exceptions

from typing import Any, Dict, Union


def raise_with_line_mapping(e: Exception, obj: Any, annotated_ast: ast.AST, source_code: str):
    """Raise the given exception with information about the original location of the exception.

    If an exception is raised in generated code, this will add a cause that describes the
    original location of the code that produced the generated code.

    Args:
        e: The exception to possibly add a cause for.
        obj: The original object from which code was generated.
        annotated_ast: The ast for the code that was generated. This should be annotated with
            `original_lineno` for the line number for which the code was generated.
        source_code: The code for `annotated_ast`.

    Raises:
        e: The original exception. If it can be determined this exception has a cause of
            a `GeneratedCodeException` that contains information about the original file and
            line number of the code that generated the code that threw the exception.
    """
    line_map = construct_line_map(annotated_ast, source_code)
    offset_lineno = inspect.getsourcelines(obj)[-1]
    original_filename = inspect.getsourcefile(obj)

    tb = e.__traceback__
    if tb is not None and tb.tb_next is not None:
        last_lineno = tb.tb_next.tb_lineno
        if last_lineno in line_map:
            # -1 from adding to 1 starting index values.
            original_line_no = offset_lineno + line_map[last_lineno] - 1
            raise e from exceptions.GeneratedCodeException(
                e, original_line_no, original_filename or "<could not determine>"
            )
    raise e


def construct_line_map(annotated_ast: gast.AST, source_code: str) -> Dict[int, int]:
    """Construct a map from the line number in generated code to the original line of the code.

    Args:
        annotated_ast: The ast for the generated code that has `original_lineno` attribute on
            each of its nodes that correspond to the location of the original code that generated
            this node.
        source_code: The source code for the given `annotated_ast`.

    Returns:
        A map from the line number in the generated code to the line number in the original code
            that generated the code.
    """
    new_ast = gast.parse(source_code)
    map: Dict[int, int] = {}

    for old, new in zip(_ast.walk_ast(annotated_ast), _ast.walk_ast(new_ast)):
        if hasattr(old, "original_lineno"):
            # We could walk parents for nodes that don't have line numbers like Load, but it
            # seems like these are always children of nodes that supply relevant line map info.
            if hasattr(new, "lineno"):
                if new.lineno in map:
                    assert (
                        map[new.lineno] == old.original_lineno
                    ), "Inconsistent line mapping, this should not occur, please file a bug."
                map[new.lineno] = old.original_lineno
    return map
