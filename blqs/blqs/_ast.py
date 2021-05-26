import ast
import gast

from typing import Union


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
