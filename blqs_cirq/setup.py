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
from setuptools import find_packages, setup

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

packages = ["blqs_cirq"] + ["blqs_cirq." + package for package in find_packages(where="blqs_cirq")]

setup(
    name=name,
    version=__version__,
    url="https://github.com/ionq/blqs_cirq",
    author="The Blqs Developers",
    author_email="dabacon@gmail.com",
    python_requires=">=3.7.0",
    install_requires=requirements,
    license="Apache 2",
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=packages,
)


# Instruction for release
# 1. Create distribution:
#   python setup.py sdist bdist_wheel
# 2. Check the distribution:
#   twine check dist/*
# 3. Upload to test pypi:
#   twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# 4. Visit https://test.pypi.org/project/blqs_cirq/ and check that it can install.
# You will need to install requirement since most of these are not on test pypi:
#   pip install -r ../blqs/requirements.txt
#   # Assuming that you have just also updated blqs do
#   pip install -i https://test.pypi.org/simple/ blqs
#   # Else
#   pip install blqs
#   # Finally
#   pip install -r requirements.txt
# Followed by pip instructions from website
#   pip install -i https://test.pypi.org/simple/ blqs_cirq
# 5. Upload to prod pypi:
#   twine upload di    st/*
# 6. Confirm on https://pypi.org/project/blqs/ and test install using pip.
