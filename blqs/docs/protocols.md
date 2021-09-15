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

####  example

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
We see that the annotation has captured the python native if statement.
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
