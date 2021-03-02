import gast


class CollectSymbols(gast.NodeVisitor):
    def __init__(self):
        self._symbols = set()

    def symbols(self):
        return frozenset(self._symbols)

    def visit_Global(self, node):
        for name in node.names:
            self._symbols.add(name)

    def visit_Nonlocal(self, node):
        for name in node.names:
            self._symbols.add(name)

    def visit_Name(self, node):
        self._symbols.add(node.id)


def collect_symbols(node):
    visitor = CollectSymbols()
    visitor.visit(node)
    return visitor.symbols()
