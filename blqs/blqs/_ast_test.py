import ast
import textwrap

import gast

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
    class

    gast_nodes = gast.parse(textwrap.dedent(code))


    ast_nodes = ast.parse(textwrap.dedent(code))
    transformed_nodes = _ast.gast_to_ast(gast_nodes)
    # No easy way to check node equality, we just check types.
    for t, a in zip(_ast.walk_ast(transformed_nodes), _ast.walk_ast(ast_nodes)):
        assert type(t) == type(a)
