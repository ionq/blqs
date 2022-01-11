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
import types
import pytest
import gast

import blqs
from blqs import decorators


def test_remove_decorator_empty():
    assert decorators._remove_decorators([], module_aliases=["m"], method_aliases=["match"]) == []


def test_remove_decorator_name():
    match_node = gast.Name("match", gast.Load(), None, None)
    nonmatch_node = gast.Name("nonmatch", gast.Load(), None, None)
    assert (
        decorators._remove_decorators([match_node], module_aliases=[], method_aliases=["match"])
        == []
    )
    assert decorators._remove_decorators(
        [nonmatch_node], module_aliases=[], method_aliases=["match"]
    ) == [nonmatch_node]
    with pytest.raises(ValueError, match="decorator"):
        decorators._remove_decorators(
            [match_node, nonmatch_node], module_aliases=[], method_aliases=["match"]
        )


def test_remove_decorator_attribute():
    match_node = gast.Attribute(gast.Name("module", gast.Load(), None, None), "match", gast.Load())
    nonmatch_node = gast.Attribute(
        gast.Name("module", gast.Load(), None, None), "nonmatch", gast.Load()
    )
    nonmatch_module_node = gast.Attribute(
        gast.Name("othermodule", gast.Load(), None, None), "match", gast.Load()
    )
    assert (
        decorators._remove_decorators(
            [match_node], module_aliases=["module"], method_aliases=["match"]
        )
        == []
    )
    assert decorators._remove_decorators(
        [nonmatch_node], module_aliases=["module"], method_aliases=["match"]
    ) == [nonmatch_node]
    assert decorators._remove_decorators(
        [nonmatch_module_node], module_aliases=["module"], method_aliases=["match"]
    ) == [nonmatch_module_node]
    with pytest.raises(ValueError, match="decorator"):
        decorators._remove_decorators(
            [match_node, nonmatch_node],
            module_aliases=["module"],
            method_aliases=["match"],
        )


def test_remove_decorator_call_name():
    match_node = gast.Call(gast.Name("match", gast.Load(), None, None), [], [])
    nonmatch_node = gast.Call(gast.Name("nonmatch", gast.Load(), None, None), [], [])
    assert (
        decorators._remove_decorators([match_node], module_aliases=[], method_aliases=["match"])
        == []
    )
    assert decorators._remove_decorators(
        [nonmatch_node], module_aliases=[], method_aliases=["match"]
    ) == [nonmatch_node]
    with pytest.raises(ValueError, match="decorator"):
        decorators._remove_decorators(
            [match_node, nonmatch_node], module_aliases=[], method_aliases=["match"]
        )


def test_remove_decorator_call_attribute():
    match_node = gast.Call(
        gast.Attribute(gast.Name("module", gast.Load(), None, None), "match", gast.Load()),
        [],
        [],
    )
    nonmatch_node = gast.Call(
        gast.Attribute(gast.Name("module", gast.Load(), None, None), "nonmatch", gast.Load()),
        [],
        [],
    )
    nonmatch_module_node = gast.Call(
        gast.Attribute(gast.Name("othermodule", gast.Load(), None, None), "match", gast.Load()),
        [],
        [],
    )

    assert (
        decorators._remove_decorators(
            [match_node], module_aliases=["module"], method_aliases=["match"]
        )
        == []
    )
    assert decorators._remove_decorators(
        [nonmatch_node], module_aliases=["module"], method_aliases=["match"]
    ) == [nonmatch_node]
    assert decorators._remove_decorators(
        [nonmatch_module_node], module_aliases=["module"], method_aliases=["match"]
    ) == [nonmatch_module_node]
    with pytest.raises(ValueError, match="decorator"):
        decorators._remove_decorators(
            [match_node, nonmatch_node],
            module_aliases=["module"],
            method_aliases=["match"],
        )


def test_remove_decorator_no_matches_leaves():
    node1 = gast.Name("one", gast.Load(), None, None)
    node2 = gast.Name("two", gast.Load(), None, None)
    assert decorators._remove_decorators(
        [node1, node2], module_aliases=["module"], method_aliases=["match"]
    ) == [node1, node2]


def test_compute_module_aliases():
    base_module = types.ModuleType("my_module")

    def func():
        pass

    base_module.func = func
    alias = base_module

    match_decorators = blqs.DecoratorSpec(module=base_module, method=base_module.func)
    assert decorators._compute_module_aliases([match_decorators], locals()) == {
        "my_module",
        "base_module",
        "alias",
    }


def test_compute_module_aliases_empty():
    base_module = types.ModuleType("my_module")

    def func():
        pass

    base_module.func = func

    match_decorators = blqs.DecoratorSpec(module=base_module, method=base_module.func)
    assert decorators._compute_module_aliases([], locals()) == set()


def test_compute_function_aliases():
    base_module = types.ModuleType("my_module")

    def func():
        pass

    base_module.func = func

    other_func = func

    match_decorators = blqs.DecoratorSpec(module=base_module, method=base_module.func)
    assert decorators._compute_method_aliases([match_decorators], locals()) == {
        "func",
        "other_func",
    }


def test_compute_function_aliases_empty():
    base_module = types.ModuleType("my_module")

    def func():
        pass

    base_module.func = func

    assert decorators._compute_method_aliases([], locals()) == set()
