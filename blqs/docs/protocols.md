# Protocols and Capture Native Python

A major motivator for blqs was to be able to write normal python code,
and then to be able to capture the intent of this code in an object
describing this code. Unfortunately Python does not allow for overriding
things like `if` or `for` statements, and thus, well, thus blqs.

As described in [concepts](concepts.md), blqs uses protocols to determine
when it should capture a python statement or to interpret it as normal
python code.  Here we describe the supported statements and the protocols
that they use.

## If Statements

If statements are captured into blqs statements if the condition in the
if statement implements the *is readable* protocol and this protocol
returns `True`.  An example of such an object is a `blqs.Register` (in its
default configuration). The protocol itself has the follow structure:
```python
class SupportsIsReadable(Protocol):
    """A protocol for objects that are readable."""

    def _is_readable_(self) -> bool:
        """Returns whether the object is readable."""
```
When the conditional part of an `if` statement implements the
`_is_readable_` method, then blqs captures the code in the conditional code
for this statement in a `blqs.If` statement. In particular, it captures
the portion which is true for the conditional in the `if_block` method
and the portion which is false for the conditional in the  `else_block`
method. See the example below.

Note that python also contains an `elif` statement. These are treated just as
they are in python, as an if statement inside an else statement. A terminal else 
is then  associated with that inner if statement.

#### If example

```python
@blqs.build
def my_program():
    op1 = blqs.Op("A")
    if blqs.Register("a"):
        op1(1)
    else:
        op1(2)

program = my_program()
print(program)
> prints
> if R(a):
>   A 1
> else:
>   A 2
```
We see that the build decorator has captured the python native if statement.
```python
for statement in program:
    print(type(statement))
> prints
> <class 'blqs.conditional.If'>
```
That statement has, in turn, captured the two instructions into an if
block and an else block:
```python
if_statement = program[0]
print(if_statement.if_block())
> prints
>   A 1
print(if_statement.else_block())
> prints
>   A 2
```

## For Statements

For statements are captured into blqs statements if the iterator portion
of the for statement supports the *is iterable* protocol. This protocol
means that they implement the `_is_iterable_` and `_loop_vars_` methods.
This protocol has the structure:
```python
class SupportsIterable(Protocol):
    """A protocol for objects that are iterable."""

    def _is_iterable_(self) -> bool:
        """Returns whether the object is iterable."""

    def _loop_vars_(self) -> Tuple:
        """Returns the object's loop variables."""
```
The iterator portion of the for statement is the `iter` in `for targets in iter:`.
The `_is_iterable_` method should return True if the object is iterable,
while the `_loop_vars_` should return the object that that will be assigned
to the targets in the for statement. In other words the `targets` in
`for targets in iter` will be assigned the `_loop_vars_`.  When blqs
captures the for loop, it stores the results in a `blqs.For` statement.

A `blqs.For` statement contains methods for getting the portions of the code that
were captured by the blqs build process. The iterator portion itself is captured
in the `iterable` method. One can get the loop variables of this iterator from the
`loop_vars` method. The code inside the for loop is then capture into a `loop_block`
method.

Finally, a little used portion of python is a `for` `else` clause statement, like
```python
found = None
for x in my_list:
    if my_list % 4 == 0:
        found = x
        break
else:
    raise NoFoundException()
```
The else portion of this code only executes in python if the for loop executes to
exhaustion. If it hits the break, it does not execute.  Blqs will capture the
else block in an `else_block`.

#### For example

```python
op = blqs.Op("A")

@blqs.build
def my_program():
    for x in blqs.Iterable("range(5)", blqs.Register("a")):
        op(x)
    else:
        op(1)

program = my_program()
print(program)
> prints
> for R(a) in range(5):
>   A R(a)
> else:
>   A 1
```
We see that the build decorator has captured a single `blqs.For` statement
```python
for statement in program:
    print(type(statement))
> prints
> <class 'blqs.loops.For'>
```
That statement has, in turn, captured the iterable and the for and else blocks
```python
for_statement = program[0]
print(for_statement.loop_block())
> prints
>   A R(a)
print(for_statement.else_block())
> prints
>   A 1
```
Notice how we have used the python `x` variable which was bound to the
`_loop_vars_` of the iterable.

## While statements

While statements are captured into blqs statements if the condition in the
while statement implements the *is readable* protocol and this protocol
returns `True`.  An example of such an object is a `blqs.Register` (in its
default configuration). The explicit protocol is:
```python
class SupportsIsReadable(Protocol):
    """A protocol for objects that are readable."""

    def _is_readable_(self) -> bool:
        """Returns whether the object is readable."""
```
When the conditional part of an `while` statement conditional supports the
*is readable* protocol, then blqs captures the code in the conditional code
for this statement in a `blqs.While` statement. In particular, it captures
the portion in the while loop and this is accessed via the `loop_block` of
the `blqs.While` object.  The `blqs.While` also capture the conditional itself,
in the `conditional` method.

In addition, while loops in python can also have an else clause. In python the else
portion executes if the while statement terminates without breaking out of the
conditional (i.e. by the conditional going false).  Blqs will also capture any
else statements in `blqs.While` object and this is accessible via the `else_block`
method.

#### While example

```python
op = blqs.Op("A")

@blqs.build
def my_program():
    while blqs.Register("a"):
        op(1)
    else:
        op(2)

program = my_program()
print(program)
> prints
> while R(a):
>   A 1
> else:
>   A 2
```
We see that the build decorator has captured a single `blqs.While` statement
```python
for statement in program:
    print(type(statement))
> prints
> <class 'blqs.loops.While'>
```
That statement has, in turn, captured the condition, loop, and else blocks
```python
while_statement = program[0]
print(while_statement.condition())
> prints
> R(a)
print(while_statement.loop_block())
> prints
>   A 1
print(while_statement.else_block())
> prints
>   A 2
```

Notice that the conditional is just an object that is readable. It is very
common to have conditionals in while statements that are expressions that
evaluate to a Truthy or Falsy value. Because python supports overriding
many of the operators used in creating expressions, i.e. `>`, `<`, `==`, etc.,
when you encounter this case you should likely use python's overloading
to capture these expressions.

## Assignment Statements

Assignments can be captured by blqs if the values that are being assigned
implement the *readable targets* protocol or implement the *is readable*
protocol.  The *readable targets* protocol is a class that implements the
`_readable_targets_` method.  This method should return ta tuple of the
objects that are readable,  This protocol has the structure
```
class SupportsReadableTargets(Protocol):
    """A protocol for objects that have readable targets."""

    def _readable_targets_(self) -> Tuple:
        """Returns the readable targets of the object."""
```
The *is readable* protocol is described above and has objects that implement
the `_is_readable_` method.  When either of these protocols is implemented
by the value in a python assign statement, blqs will capture this into an
`blqs.Assign` statement.  The assign object captures the names of the variables
being assigned. This is accessible vi the `assign_names` method of the assign
object.  It also captures the readable targets, and these are accessible via
the `value` method of the object.  Note that this supports assigning single
variables, but also assigning tuples, i.e. `a, b = 1, 2`.  In addition
to the assign statement, the actual variables being assigned to are also
correctly assigned with the right-hand side (the readable targets).

#### Assignment example

```python
op = blqs.Op("A")

@blqs.build
def my_program():
    b = blqs.Register("b")
    op(b)

program = my_program()
print(program)
> prints
> b = R(b)
> A R(b)
```
Notice how the python variable b is bound to the register object, and can be
used later, just as it would in any normal python program.  We can see that
the decorator has captured the assignment:
```python
for statement in program:
    print(type(statement))
> prints
> <class 'blqs.assignment.Assign'>
> <class 'blqs.instruction.Instruction'>
```
The `blqs.Assign` object has captured the target and value of the assignment:
```python
assign_statement = program[0]
print(assign_statement.assign_names())
> prints
> ('b', )
print(assign_statement.value())
> prints
> R(b)
```

One interesting part of blqs is that `blqs.Instruction`s will return targets
that are readable when calling `_readable_targets_` on the instruction.
```python
meas = blqs.Op("MEAS")

@blqs.build
def my_program():
    a = meas(0, blqs.Register("a"))

program = my_program()
print(program)
> prints
> MEAS 0, R(a)
> a = MEAS 0, R(a)
```
Notice that it creates two statements, the instruction, and then the assignment.
This shorthand can be useful for building instructions with "return values".

## Del Statements

Delete statements can be captured in blqs if the variables being deleted
corresponds with objects supporting the *is deletable* protocol.  Classes that
implement the  *is deletable* protocol implement the method `_is_deletable_`
and return true. The explicit protocol is
```
class SupportsIsDeletable(Protocol):
    """A protocol for object that can be deleted."""

    def _is_deletable_(self) -> bool:
        """Returns whether the object is deletable."""
```
Blqs will capture the variables in a `del` statement in a `blqs.Delete` statement.
This will capture all objects that support the *is deletable* protocol, and
will delete all the objects that do not.  Note that both can exist in a
single `del` statement.  When it captures, the variable names that are deleted
are captured in the `blqs.Delete` statement and accessible via the `delete_names`
method.

#### Del example

```python
@blqs.build
def my_program():
    x = blqs.Register("a")
    y = 1
    del x, y

program = my_program()
print(program)
> prints
> x = R(a)
> del x
```
Notice that the `del` of `y` is not captured, because it is not a *is deletable*
object. When `my_program` is called, however, `y` is in fact deleted at the line
that executes the `del`.

We see that the second statement is indeed a `blqs.Delete` statement
```python
for statement in program:
    print(type(statement))
> prints
> <class 'blqs.assignment.Assign'>
> <class 'blqs.delete.Delete'>
```
And that it has captured the name of the variable being deleted
```python
del_statement = program[1]
print(del_statement.delete_names())
> prints
> ('x', )
```

## Learn More

* [Intro](intro.md)
* [Concepts](concepts.md)
