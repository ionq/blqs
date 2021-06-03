import textwrap

import gast


class ReplacementTransformer(gast.NodeTransformer):
    def __init__(self, **replacements):
        self.replacements = replacements

    def visit_Name(self, node):
        if node.id in self.replacements:
            replacement = self.replacements[node.id]
            if isinstance(replacement, str):
                node.id = replacement
            else:
                return replacement
        return node

    def visit_FunctionDef(self, node):
        node = self.generic_visit(node)
        if node.name in self.replacements:
            node.name = self.replacements[node.name]
        return node

    def visit_Expr(self, node):
        # If we changed things, return it outside of an expression.
        visited_node = self.visit(node.value)
        if visited_node is node.value:
            return node
        return visited_node


def replace(template, **replacements):
    """A simple templating system.

    Rules:

        * Replaces `Name` nodes with either the nodes that are the replacements, or if
            the replacement is a string replaces the id of the `Name`.

        * Replaces the name of a `FunctionDef` with a possible string replacement.

        * Replaces an `Expr` wholesale with the supplied replacement nodes.

    Args:
        template: A string containing python code. The code can have placeholder names
            that will be replaced by this call.
        replacements: Keyword arguments from the placeholder name in the code to the `gast.Node`,
            a sequence of the `gast.Node`s representing the code that should be replaced,
            or a string, which is used to replace an `id` or `name` as described above.

    Returns:
        A list of the `gast.Node`s representing the template with replaced nodes.
    """
    nodes = gast.parse(textwrap.dedent(template))
    transformer = ReplacementTransformer(**replacements)
    replaced_nodes = transformer.visit(nodes)
    return replaced_nodes.body
