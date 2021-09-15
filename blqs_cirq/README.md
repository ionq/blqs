# blqs_cirq: Taking the pain out of writing Cirq programs

Blqs_cirq is a library that uses blqs to make it easier to write Cirq programs.

Here is the creation of a simple circuit in Cirq
```python
import cirq
circuit = cirq.Circuit()
q0, q1 = cirq.LineQubit.range(2)
circuit.append(cirq.H(q0))
circuit.append(cirq.CX(q0, q1))
circuit.append(measure(q0, key='a'))
```
Blqs-cirq makes it so that you can write this more like a normal imperative
program
```python
import blqs_cirq as bc
from blqs_cirq import CX, H, measure

# Write the function imperatively.
@bc.build
def my_circuit():
    H(0)
    CX(0, 1)
    measure(q0, key='a')

# To create the circuit we simply call the function.
circuit = my_circuit()
```

Blqs provides supports for all of the gates in Cirq, along with all of the various ways to use
these gates to create operations.

But wait, there is more.  Blqs_cirq supports

* Simplification of qubit specification.  Instead of creating `LineQubit` or `NamedQubit`, etc,
one can simply use integers (converted to `LineQubit`s), 2-tuples or 2-lists (converted to
`GridQubit`s) or strings (converted to `NamedQubits`). Custom conversions are also possible.

* Simplification of control flow primitives. For example Cirq currently supports a subcircuit
which can be repeated. For example here we repeat a small circuit within our circuit:
```python
@bc.build
def my_circuit():
    H(1)
    with Repeat(repetitions=10):
        H(0)
        CX(0, 1)
```

* Support for Cirq's insertion strategies:
```python
@bc.build
def my_circuit():
    with bc.InsertStrategy(cirq.InsertStrategy.NEW):
        H(0)
        H(1)
```

# Installation

TODO

# Documentation

TODO
