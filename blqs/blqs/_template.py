import gast


class ReplacementTransformer(gast.NodeTransformer):
    def __init__(self, **replacements):
        self.replacements = replacements

    def visit_Name(self, node):
        if node.id not in self.replacements:
            return node
        return self.replacements[node.id]


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
    nodes = gast.parse(template)
    transformer = ReplacementTransformer(**replacements)
    replaced_nodes = transformer.visit(nodes)
    return replaced_nodes
