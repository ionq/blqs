import ast
import textwrap

import gast
import pytest

from blqs import _ast


def test_walk_ast():
    code = """
    if a:
        print(\"a\")
    else:
        b = 1
    """
    nodes = gast.parse(textwrap.dedent(code))

    order = [
        gast.Module,
        gast.If,
        gast.Name,
        gast.Load,
        gast.Expr,
        gast.Call,
        gast.Name,
        gast.Load,
        gast.Constant,
        gast.Assign,
        gast.Name,
        gast.Store,
        gast.Constant,
    ]
    for node, cls in zip(_ast.walk_ast(nodes), order):
        assert isinstance(node, cls)


def test_gast_to_ast():
    code = """
    a: int = 1
    for x in range(5):
        print(x)
    else:
        b = 2
    """
    gast_nodes = gast.parse(textwrap.dedent(code))
    ast_nodes = ast.parse(textwrap.dedent(code))
    transformed_nodes = _ast.gast_to_ast(gast_nodes)
    # No easy way to check node equality, we just check types.
    for t, a in zip(_ast.walk_ast(transformed_nodes), _ast.walk_ast(ast_nodes)):
        assert type(t) == type(a)


def test_gast_to_ast_annotations():
    code = """
    a: int = 1
    for x in range(5):
        print(x)
    else:
        b = 2
    """

    class AnnotateNamesWithLineNos(gast.NodeTransformer):
        def visit(self, node):
            new_node = super().visit(node)
            if type(new_node) == gast.Name:
                setattr(new_node, "original_lineno", node.lineno)
            return new_node

    gast_nodes = gast.parse(textwrap.dedent(code))
    annotated_nodes = AnnotateNamesWithLineNos().visit(gast_nodes)

    transformed_nodes = _ast.gast_to_ast(annotated_nodes)
    for node in _ast.walk_ast(transformed_nodes):
        if type(node) == ast.Name:
            assert node.original_lineno == node.lineno
        else:
            assert not hasattr(node, "original_lineno")


def test_construct_line_map():
    code = """
    a: int = 1
    for x in range(5):
        print(x)
    else:
        b = 2
    """

    class AnnotateWithDoubleLineNos(gast.NodeTransformer):
        def __init__(self):
            self.original_linenos = set()

        def visit(self, node):
            new_node = super().visit(node)
            if hasattr(new_node, "lineno"):
                self.original_linenos.add(new_node.lineno)
                setattr(new_node, "original_lineno", 2 * new_node.lineno)
            return new_node

    source = textwrap.dedent(code)
    gast_nodes = gast.parse(source)
    transformer = AnnotateWithDoubleLineNos()
    annotated_nodes = transformer.visit(gast_nodes)

    line_map = _ast.construct_line_map(annotated_nodes, source)
    for key, value in line_map.items():
        assert value == 2 * key
    assert set(line_map.keys()) == transformer.original_linenos


def test_construct_line_map_inconsistent_linenos():
    code = """
    a = 1
    """
    source = textwrap.dedent(code)
    gast_nodes = gast.parse(source)
    gast_nodes.body[0].targets[0].original_lineno = 2
    gast_nodes.body[0].value.original_lineno = 1

    with pytest.raises(AssertionError, match="Inconsistent"):
        _ast.construct_line_map(gast_nodes, source)
