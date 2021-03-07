
# blqs: Building Blocks for Quantum Languages

Blqs is a framework for writing quantum programs that look like native Python
programs.

In many traditional quantum programming frameworks on writes a quantum program
via appending to a container object, (here is an example from Cirq):
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
def hello_blqs()
    H(0)
    CX(0, 1)

program = hello_blqs()
print(program)
> prints
> H 0
> H 1
```
Here `program` is `blqs.Program` container of the listed `blqs.Statement`s. The
function annotation turns that function into a builder that when called returns
the built program.

More interestingly, blqs programs can also take native python functionality,
like `if` statements, and capture then in blqs objects:
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

print(hello_if_blqs)
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

Further we can mix and match native and captured python.
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
frameworks.  As such, blqs itself will be kept very simple and pure, other frameworks
will be built on top of it.

The inspiration for blqs comes from Tensorflow's autograph library.
