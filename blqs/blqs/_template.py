import gast
import textwrap


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


def replace(template, **replacements):
    """A simple templating system.

    Args:
        template: A string containing python code. The code can have placeholder names
            that will be replaced by this call.
        replacements: Keyword arguments from the placeholder name in the code to the `gast.Node`
            or a sequence of the `gast.Node`s representing the code that should be replaced.

    Returns:
        A list of the `gast.Node`s representing the template with replaced nodes.
    """
    nodes = gast.parse(textwrap.dedent(template))
    transformer = ReplacementTransformer(**replacements)
    replaced_nodes = transformer.visit(nodes)
    return replaced_nodes
