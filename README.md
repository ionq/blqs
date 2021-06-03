# blqs: Building Blocks for Domain Specific Languages

.. image:: https://github.com/ionq/blqs/workflows/Continuous%20Integration/badge.svg
  :target: https://github.com/ionq/blqs
  :alt: Build Status

Blqs is a framework for building domain specific language that can be written in native Python.
It was inspired by TensorFlow's
[autograph](https://blog.tensorflow.org/2018/07/autograph-converts-python-into-tensorflow-graphs.html)
library, and motivated by attempting to improve quantum computing programming frameworks like
[Cirq](https://quantumai.google/cirq) and [Qiskit](https://qiskit.org).

# Packages

This repo contains two packages, follow the links for installation instructions and documentation.

* [blqs](blqs) The base blqs framework.
* [blqs_cirq](blqs_cirq) An application to blqs to [Cirq](https://quantumai.google/cirq)

# Contributing



# Motivating example

Here is a motivating example.  In many traditional quantum programming frameworks one writes
a quantum program via appending to a container object, (here is an example from Cirq):
```python
import cirq
circuit = cirq.Circuit()
q0, q1 = cirq.LineQubit.range(2)
circuit.append(cirq.H(q0))
circuit.append(cirq.CX(q0, q1))
```
In blqs instead one can define functions that return programs.
```python
import blqs

H = blqs.Operand('H')
CX = blqs.Operand('CX')

@blqs.build
def hello_blqs():
    H(0)
    CX(0, 1)

program = hello_blqs()
print(program)
> prints
> H 0
> H 1
```
Here `program` is `blqs.Program` container of the listed `blqs.Statement`s. The
function annotation turns the `hello_blqs` function into a builder that,
 when called, returns the built program.

More interestingly, blqs programs can also take native python functionality,
like `if` statements, and capture them in blqs objects:
```python
M = blqs.Operand('M')

def hello_if_blqs():
    a = blqs.Register('a')
    H(0)
    M(0, 'a')
    if a:
        CX(0, 1)
    else:
        CX(1, 0)

program = hello_if_blqs()
print(program)
> prints
> H 0
> M 0,a
> if a:
>     CX 0,1
> else:
>     CX 1,0

# This is three statements, the last having captured the if.
for s in program:
    print(type(s))
> prints
> <class 'blqs.instruction.Instruction'>
> <class 'blqs.instruction.Instruction'>
> <class 'blqs.conditional.If'>
```

Further we can mix and match native and captured Python. For example,
here `a` is just a normal python boolean variable, and we
can use it in to build one of two different cases:
```python

def hello_native(a):
    if a:
        H(0)
    else:
        H(1)
print(hello_native(True))
> prints
> H 0
print(hello_native(False))
> prints
> H 1
```

Blqs is meant to be all about building programs and the intermediate representation
of that program.  In many ways it is meant to be a framework to help you build other
frameworks.  As such, every attempt will be made to keep blqs simple, the ideas is that other
frameworks can be built on top of it.
