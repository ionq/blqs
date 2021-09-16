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

import io
from setuptools import setup

# Read the __version__.
__version__ = ""
exec(open("blqs_cirq/_version.py").read())
# Sanity check
assert __version__, "Version string cannot be empty"

name = "blqs_cirq"

description = "A library for writing imperative quantum computing programs in Cirq."

long_description = io.open("README.md", encoding="utf-8").read()

requirements = open("requirements.txt").readlines()
requirements = [r.strip() for r in requirements]

packages = [
    "blqs_cirq",
]

setup(
    name=name,
    version=__version__,
    url="https://github.com/ionq/blqs_cirq",
    author="The Blqs Developers",
    author_email="bacon@ionq.com",
    python_requires=(">=3.7.0"),
    install_requires=requirements,
    licence="Apache 2",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=packages,
)
