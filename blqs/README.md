# blqs: Building Blocks for Domain Specific Languages

Blqs is a framework for building (internal) domain specific language that can be written
in Python. It was inspired by TensorFlow's autograph library, and motivated by the state of
the art (circa 2021) in quantum programming frameworks like Cirq and Qiskit.

In short blqs let you define domain specific languages and gives you access to use native
Python features like `if`, `while`, or `for` in these languages. This fills in a missing
feature for Python, which while they do have operator overloading, does not allow for
overloading these built in constructions.

Example:
```python
import blqs
H, M, CX = blqs.Op('H'), blqs.Op('M'), blqs.Op('CX')

@blqs.build
def hello_blqs():
    a = blqs.Register('a')
    H(0)
    M(0, 'a')
    if a:
        CX(0, 1)
    else:
        CX(1, 0)
```
Then, if we call this method, we will produce a `blqs.Program` that includes both statements,
like `H(0)` but also the `if` and `else` statements.
```python
program = hello_blqs()
for s in program:
    print(type(s))
> prints
> <class 'blqs.instruction.Instruction'>
> <class 'blqs.instruction.Instruction'>
> <class 'blqs.conditional.If'>
```
Where the last statement contains blocks that hold the `CX` statements.

# Installation

To install blqs one can simply pip install the appropriate package
```
pip install blqs
```
See [requirements.txt](requirements.txt) for the dependencies that blqs will
pull in.

# Documentation

A good place to get started is to read the [introduction to blqs](docs/intro.md).
After that, the ideas and abstractions in blqs are described in the
[concepts guide](docs/concepts.md). To learn about support for capturing native
python code, see refer to the [protocols section](docs/protocols.md) of the docs.
For a quick intro via a jupyter notebook, see [hello blqs](hello_blqs.ipynb).
