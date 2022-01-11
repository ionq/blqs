# Features

## Gates, gate methods, and factories

Blqs_cirq aims to retain all the gates with identical notation to the
latest version of Cirq.  This means that all `cirq.Gate` subclasses
are supported (modulo some private gates and a few odd exceptions).
So for `cirq.H` there is a `bc.H`, and `cirq.CNOT` there is a `bc.CNOT`,
etc.  These gates all appear at the top level of `blqs_cirq`. Gates from
non-core Cirq, such as gates in `cirq_google` or `contrib` appear in
their own namespaces, i.e. `blqs_cirq.google` and `blqs_cirq.contrib`,
respectively.  The blqs_cirq version of these objects are `blqs_cirq.CirqBlqsOp`s.
Note that blqs_cirq supports not gates that are not just unitaries or measurements,
but also cirq's channel gates.

Cirq also constructions some `cirq.Operation`s directly via helper methods.
An example of this is `cirq.measure`, which takes in qubits along with a `key`
parameter describing the key and produces the `cirq.Operation` that acts on
these qubits with a `cirq.MeasurementGate`.  Blqs_cirq also supports these
methods.  `bc.measure(0, key='x')` is equivalent to `cirq.measure(cirq.LineQubit(0), key='x')`.

Finally, there are some stranger patterns in Cirq which are supported. For example
`cirq.SingleQubitCliffordGate` has class variable constants like
`cirq.SingleQubitCliffordGate.H`.  Blqs_cirq has the equivalent `bc.SingleQubitCliffordGate.H`.

Blqs_cirq has support for all of Cirq's gates, but if you have your own gate,
you can also use blqs_cirq to easily create a blqs_cirq version of that gate.
To do this simply call `blqs.create_cirq_blqs_op` on the gate. If you have a method
that takes qubits to produce a `cirq.Operation` you can also transform it using this
method.

## Qubit decoding

In cirq qubits or qudits are represented by subclasses of the `cirq.Qid` class.
Common examples of these are `cirq.NamedQubit`, `cirq.LineQubit`, and
`cirq.GridQubit`. Because these are used so often, in blqs_cirq we use
the natural versions of these as targets of gates.

* `int`s are treated as `cirq.LineQubit`s. Example: `bc.H(0)` is equivalent to `cirq.H(cirq.LineQubit(0))`.

* `str`s are treated as `cirq.NamedQubit`s. Example: `bc.H("a")` is equivalent to `cirq.H(cirq.NamedQubit("a"))`.

* `tuple`s or `lists` of length two are treated as `cirq.GridQubit`s. Example `bc.H((0, 1))` is equivalent to `cirq.H(cirq.GridQubit(0, 1))

* `Qid`s will be passed along if they are supplied `bc.H(cirq.LineQubit(0))` is equivalent to `cirq.H(cirq.LineQubit(0))`.

* Any other object that does not obey the above rules is used as a target will
be converted to a `cirq.NamedQubit` with the name `str(object)`.

Further, if necessary, one can supply your own qubit decoder as config to
`blqs_cirq.build_with_config` for your own custom decoder to `cirq.Qid` objects.

## Circuit Operations

In cirq, a `cirq.CircuitOperation` is an operation corresponding to a subcircuit.
These can be nested. Right now this is one of the few primitives that are not
unrolled circuits in Cirq.  Writing these in cirq is a bit of a pain, since
you have to create the subcircuit, freeze it, then create the `CircuitOperation`.
Blqs_cirq supports this via some simple context managers.

If you just want a subcircuit that repeats, one can directly use the `blqs_cirq.Repeat`
context manager:
```python
@bc.build
def my_program():
    with bc.Repeat(repetitions=10):
        bc.H(0)

program = my_program()
print(program)
> prints
> 0: ───Circuit_0x2cde651793fc45a6:─────────────
>       [ 0: ───H───              ](loops=10)
```
For access to more of the parameters of `cirq.CircuitOperation` beyond just
`repetitions`, one can use the `blqs_cirq.CircuitOperation` context manager.

## Insert strategy

When creating `cirq.Circuit`s one can use different `cirq.InsertStrategy`s. The
change how the stream of operations being fed into the circuit via append are
added to the circuit. Cirq's default insertion strategy is `EARLIEST` and this
is what blqs_cirq uses by default. However, if one want to use one of the other
insert strategies, one can switch over to do this by using the `cirq.InsertStrategy`
context manager.

For example to use the NEW insert strategy one would do
```python
@bc.build
def my_program():
    with bc.InsertStrategy(cirq.InsertStrategy.NEW):
        bc.H(0)
        bc.H(1)

program = my_program()
print(program)
> prints
> 0: ───H───────
>
> 1: ───────H───
```
Note that insert strategies cannot be nested, as it is not clear what this
means.
