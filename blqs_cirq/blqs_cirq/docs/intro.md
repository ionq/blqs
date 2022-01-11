 # Introduction to Blqs_cirq

Blqs_cirq is a python library that uses blqs to make writing
(Cirq)[https://github.com/quantumlib/cirq] programs more imperative and,
hopefully, more straightforward.

## A Quick Review of Cirq Circuits

In Cirq a `cirq.Circuit` is a container for `cirq.Moment`s. Each `cirq.Moment`
roughly corresponds to a slide of abstract time. A moment itself is made up
of `cirq.Operation`s, each of which operates on disjoint `cirq.Qid`s.

For example, here is a simple circuit created in Cirq:
```python
import cirq

q0, q1 = cirq.LineQubit.range(2)

circuit = cirq.Circuit()
circuit.append(cirq.H(q0))
circuit.append(cirq.CNOT(q0, q1))
circuit.append(cirq.measure(q0, q1, key="m"))
print(circuit)
> prints
> 0: ───H───@───M('m')───
>           │   │
> 1: ───────X───M────────
```
This circuit represents a Hadamard gate acting on the first qubit, a
controlled NOT from the first qubit to the second, and then a measurement
on the last two qubits storing the result in the `m` key.

Cirq comes with a large number of standard quantum gates and is easily
extensible to add your own gates. Circuit objects can then be used in other
ways by Cirq. For example, they can be optimized (compiled) into other circuits.
Or they can be simulated using built in Cirq simulator or externally available
simulators. They can also be sent to a quantum computer to run the
actual program.

Cirq has a few ways to simplify writing circuits.  One of these is that one
can take use generators to stream gates into a `cirq.Circuit` object
```python
def my_circuit():
    for q in cirq.LineQubit.range(3):
        yield cirq.H(q)

circuit = cirq.Circuit()
circuit.append(my_circuit())
print(circuit)
> prints
> 0: ───H───
>
> 1: ───H───
>
> 2: ───H───
```
This is nice as it allows for mixing of native python with the actual circuit
construction.  However, it is still a bit awkward.

Another important construction in Cirq are the basic of control flow (this
is currently, as of Cirq v0.12 a work in progress).  For example one can add
a subcircuit to Cirq which repeats a circuit multiple times
```python
q0, q1 = cirq.LineQubit.range(2)
circuit = cirq.Circuit()

subcircuit = cirq.Circuit()
subcircuit.append([cirq.H(q0), cirq.CNOT(q0, q1)])

circuit.append([cirq.H(q0), cirq.H(q1)])
circuit.append(cirq.CircuitOperation(subcircuit.freeze(), repetitions=10))
print(circuit)
> prints
>           Circuit_0xb2d97d2cac98317c:
> 0: ───H───[ 0: ───H───@───          ]─────────────
>           [           │             ]
>           [ 1: ───────X───          ](loops=10)
>           │
> 1: ───H───#2──────────────────────────────────────
```
This is rather cumbersome, and as more control flow is added to Cirq,
this is likely to make writing Cirq more painful.

# Blqs_cirq

In blqs_cirq we can do the above, in a more familiar imperative style.
```python
import blqs_cirq as bc
from blqs_cirq import H, CX

@bc.build
def my_circuit():
    H(0)
    CX(0, 1)

circuit = my_circuit()
print(circuit)
> prints
> 0: ───H───@───
>           │
> 1: ───────X───
```
My using the `blqs_cirq.build` annotation on a function, we have turned
it into a function that will return the `cirq.Circuit` corresponding to
the imperatively written circuit inside the function.  Further we have
used the `blqs_cirq` gates, `H` and `CX`, directly corresponding to the
Cirq gates, to construct the circuit.  Finally, note that instead of
using line qubits, we have used simple integers.  If we example the circuit
that has been constructed we can see that it has converted these `int`s
to `cirq.LineQubit`s.

Similarly, we can use blqs_cirq to write `cirq.CircuitOperation`s in a
cleaner form
```python
@bc.build
def my_circuit():
    H(0)
    CX(0, 1)
    with bc.Repeat(repetitions=10):
        for i in range(2):
            H(i)

circuit = my_circuit()
print(circuit)
> prints
>               Circuit_0x91d1c5891174e662:
> 0: ───H───@───[ 0: ───H───              ]─────────────
>           │   [                         ]
>           │   [ 1: ───H───              ](loops=10)
>           │   │
> 1: ───────X───#2──────────────────────────────────────
```

Behind the scenes, blqs_cirq is using blqs which is turn capturing
the

# Learn More

* [Features](features.md)
