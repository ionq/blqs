# Protocols and Capture Native Python

A major motivator for blqs was to be able to write normal python code,
and then to be able to capture the intent of this code in an object
describing this code. Unforutnately Python does not allow for overriding
things like `if` or `for` statements, and thus, well, thus blqs.

As described in [concepts](concepts.md), blqs uses protocols to determine
when it should capture a python statement or to interpret it as normal
python code.  Here we describe the supported statements and the protocols
that they use.

## If statements

If statements are captured into blqs statements if the condition in the
if statement supports the `SupportsIsReadable` protocol and this protocol
returns `True`.  An example of such an object is a `blqs.Register` (in its
default configuration).
```python
class SupportsIsReadable(Protocol):
    """A protocol for objects that are readable.

    Readable objects can be used in conditionals and loops.
    """

    def _is_readable_(self) -> bool:
        """Returns whether the object is readable."""
```
When the conditional part of an `if` statement conditional `is_readable`, then
blqs captures the code in the conditional code for this statement in a
`blqs.If` statement. In particular it captures the portion which is true for
the conditional in the `if_block` of that statement and the portion which is
false for the conditional in the `else_block`. See the example below.

Note that python also contains an `elif` statement. These are treated just as
they are in python, as an if statement inside of an else. A terminal else is then
associated with that inner if statement.

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

## For statements

For statements are captured into blqs statements if the iterator portion
of the for statement supports the `_is_iterable_` and `_loop_vars_` methods.
Classes that support these methods implement the `SupportsIterable` protocol.
```python
class SupportsIterable(Protocol):
    """A protocol for objects that are iterable.

    Iterable objects can be used in for loops.
    """

    def _is_iterable_(self) -> bool:
        """Returns whether the object is iterable."""

    def _loop_vars_(self) -> Tuple:
        """Returns the objects loop variables."""
```
The iterator portion of the for statement is the `iter` in `for targets in iter:`.
The `_is_iterable_` method should return True if the object is iterable,
while the `_loop_vars_` should return the object that that will be assigned
to the targets in the for statement. In other words the `targets` in `for targets in iter`
will be assigned the `_loop_vars_`.  When blqs captures the for loop, it stores
the results in a `blqs.For` statement.

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
exhaustion, if it hits the break, it does not execute.  Blqs will capture the
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

