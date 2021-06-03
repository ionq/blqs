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
import ast
from typing import Dict, Union

import gast


ANNOTATIONS = ["original_lineno"]


def walk_ast(node: Union[ast.AST, gast.AST]):
    """Walk an abstract syntax tree in depth first order."""
    yield node
    for n in gast.iter_child_nodes(node):
        for m in walk_ast(n):
            yield m


def gast_to_ast(gast_root: gast.AST):
    """Convert an abstract syntax tree from gast to one in ast, preserving annotations."""
    ast_root = gast.gast_to_ast(gast_root)

    for ast_node, gast_node in zip(walk_ast(ast_root), walk_ast(gast_root)):
        for annotation in ANNOTATIONS:
            lineno = getattr(gast_node, annotation, None)
            if lineno is not None:
                setattr(ast_node, annotation, lineno)
    return ast_root


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
    line_map: Dict[int, int] = {}

    for old, new in zip(walk_ast(annotated_ast), walk_ast(new_ast)):
        if hasattr(old, "original_lineno"):
            # We could walk parents for nodes that don't have line numbers like Load, but it
            # seems like these are always children of nodes that supply relevant line map info.
            if hasattr(new, "lineno"):
                if new.lineno in line_map:
                    assert (
                        line_map[new.lineno] == old.original_lineno
                    ), "Inconsistent line mapping, this should not occur. Please file a bug."
                line_map[new.lineno] = old.original_lineno
    return line_map
