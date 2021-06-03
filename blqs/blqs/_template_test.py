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
import gast
import astunparse

from blqs import _template


def test_replace_deindent():
    nodes = _template.replace("a = 1", a="b")
    assert astunparse.unparse(nodes).strip() == "b = 1"

    nodes = _template.replace("  a = 1", a="b")
    assert astunparse.unparse(nodes).strip() == "b = 1"

    template = """
    a = 1
    c = 2
    """
    nodes = _template.replace(template, a="b")
    assert astunparse.unparse(nodes).strip() == "b = 1\nc = 2"

    template = """
    if a:
        pass
    """
    nodes = _template.replace(template, a="b")
    assert astunparse.unparse(nodes).strip() == "if b:\n    pass"


def test_replace_lnames():
    nodes = _template.replace("a = 1", a="b")
    assert astunparse.unparse(nodes).strip() == "b = 1"

    nodes = _template.replace("a = 1", a="cab")
    assert astunparse.unparse(nodes).strip() == "cab = 1"

    nodes = _template.replace("a = 1", a="a")
    assert astunparse.unparse(nodes).strip() == "a = 1"


def test_replace_lnames_with_names():
    nodes = _template.replace(
        "a = 1", a=gast.Name("b", gast.Load(), annotation=None, type_comment=None)
    )
    assert astunparse.unparse(nodes).strip() == "b = 1"

    nodes = _template.replace(
        "a = 1", a=gast.Name("a", gast.Load(), annotation=None, type_comment=None)
    )
    assert astunparse.unparse(nodes).strip() == "a = 1"


def test_replace_multiple_lnames():
    nodes = _template.replace("a = 1\nc = 2", a="b", c="d")
    assert astunparse.unparse(nodes).strip() == "b = 1\nd = 2"

    nodes = _template.replace("a = 1\nc = 2\nd=3", a="b", c="d")
    assert astunparse.unparse(nodes).strip() == "b = 1\nd = 2\nd = 3"


def test_replace_multiple_lnames_with_names():
    nodes = _template.replace(
        "a = 1\nc = 2",
        a=gast.Name("b", gast.Load(), annotation=None, type_comment=None),
        c=gast.Name("d", gast.Load(), annotation=None, type_comment=None),
    )
    assert astunparse.unparse(nodes).strip() == "b = 1\nd = 2"


def test_replace_expr():
    nodes = _template.replace("a * c", a="b")
    assert astunparse.unparse(nodes).strip() == "(b * c)"

    nodes = _template.replace("a * a", a="b")
    assert astunparse.unparse(nodes).strip() == "(b * b)"

    nodes = _template.replace("a * c + a", a="b")
    assert astunparse.unparse(nodes).strip() == "((b * c) + b)"


def test_replace_expr_with_name():
    nodes = _template.replace(
        "a * c", a=gast.Name("b", gast.Load(), annotation=None, type_comment=None)
    )
    assert astunparse.unparse(nodes).strip() == "(b * c)"


def test_replace_param():
    nodes = _template.replace("f(a)", a="b")
    assert astunparse.unparse(nodes).strip() == "f(b)"


def test_replace_param_with_name():
    nodes = _template.replace(
        "f(a)", a=gast.Name("b", gast.Load(), annotation=None, type_comment=None)
    )
    assert astunparse.unparse(nodes).strip() == "f(b)"


def test_replace_single_expr():
    nodes = _template.replace("placeholder", placeholder=gast.parse("a = 1").body[0])
    assert astunparse.unparse(nodes).strip() == "a = 1"
    assert isinstance(nodes[0], gast.Assign)


def test_replace_single_expr_multiple_nodes():
    multiple_nodes = [gast.parse("a = 1").body[0], gast.parse("b = 1").body[0]]
    nodes = _template.replace("placeholder", placeholder=multiple_nodes)
    assert astunparse.unparse(nodes).strip() == "a = 1\nb = 1"


def test_replace_fn():
    fn_code = """
    def f():
        pass
    """
    nodes = _template.replace(fn_code, f="new_f")

    assert astunparse.unparse(nodes).strip() == "def new_f():\n    pass"

    fn_code = """
    def f():
        pass
    """
    nodes = _template.replace(fn_code, g="new_g")
    assert astunparse.unparse(nodes).strip() == "def f():\n    pass"
