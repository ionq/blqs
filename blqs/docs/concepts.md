# Concepts

Here we explain some main concepts in blqs.

The main goal of blqs is to allow one to write Python code, and for this code to
be capture into an object which one can then process to get meaning (semantics)
to this code.  Before jumping into this it is interesting to examine ways to do
this without using blqs.  Two of the patterns that you might encounter to
achieve this are builders and containers. For example in a builder pattern you
might do something like
```python
my_program = MyBuilder().statement1().statement2().build()
```
corresponding to some sort of program like
```
statement1
statement2
```
In the container version of this one could do something like
```python
my_program = MyProgram()
my_program.append(Statement1())
my_program.append(Statement2())
```
Both of these work, but are slightly annoying.  For the builder pattern, one ends
up formatting these with parenthesis to deal with Python's indent pattern and
long lines (whereas this is not true of languages like Java or C++), i.e.
```python
my_program = (MyBuilder()
              .statement1()
              .statement2()
              .statement3()
              .statement4())
```
Worse when one starts to create control flow, things start to get crazy
```python
my_program = (MyBuilder()
              .statement1()
              .if_statement(LessThan(x, 1))
              .then_block(MyBuilder().statement1())
              .else_block(MyBuilder().statement2().statement3())
```
A similar problem occurs over in container land. In blqs we want to alleviate 
this problem and allow one to write
```
Statement1()
if x < 1:
   Statement1()
else:
    Statement2()
    Statement3()
```
where each of these statements are Python objects, and we are able to capture
the if statement in our program.

## Programs, Statements, and Blocks

Given this discussion, it is not surprising to discover that in blqs, *statements*
are the basic building blocks of a *program*.  A statement roughly corresponds to
a line of code in a program.  A program is then an ordered container of statements
(it turns out that a program is also a statement, but more on this in a second).
This means, for example that we can create statements, and add them to a program
```python
s1 = blqs.Statement()
s2 = blqs.Statement()
p = blqs.Program()
p.append(s1)
p.append(s2)
print(p)
> prints something like
> <blqs.statement.Statement object at 0x1113426d0>
> <blqs.statement.Statement object at 0x111342670>
print(len(p))
> prints
> 2
```
This isn't that different from the container code above! But the key is that
while we can build up programs out of statements this way, we could also write
this in an imperative form in a function, and using the `blqs.build` decorator,
we can transform this form into something that returns the program corresponding
to these statements:
```python
@blqs.build
def my_program():
    blqs.Statement()
    blqs.Statement()

program = my_program()
print(type(program))
> prints
> <class 'blqs.program.Program'>

print(program)
> prints something like
> <blqs.statement.Statement object at 0x11130da60>
> <blqs.statement.Statement object at 0x11130d1f0>
```

A program is a container for statements, which can be iterated over.  Actually,
a program is an example of a more general structure, a *block*.  Blocks are containers
for statements, and a program is a block.  Blocks, however, are more general, and can
be nested within each other and even appear as parts of other statements.  A program
is a block, but one that only appears on at the top level of any block nesting.

```python
@blqs.build
def my_block():
    blqs.Statement()
    blqs.Statement()

@blqs.build
def my_program():
    blqs.Statement()
    my_block()

program = my_program()
print(program)
> prints something like
> <blqs.statement.Statement object at 0x102ea4220>
>   <blqs.statement.Statement object at 0x102f6da90>
>   <blqs.statement.Statement object at 0x102f6daf0>
```
where we see that the block of codes is indented and if we iterate over the program
```python
for statement in program:
    print(type(statement))
> prints something like
> <class 'blqs.statement.Statement'>
> <class 'blqs.block.Block'>
```
we see that the second statement is a block.

## Ops and Instructions

Above we have seen some simple programs and block with statements.  In general,
you will want to create your own classes that correspond to statements.  A common
pattern in many domain specific languages creates statements via *instructions*.
An *instruction* is an op code, called an *op* in blqs, along with the operands,
called *targets* in blqs, upon which the op code acts.

To support this `blqs` has the classes `Op` and `Instruction`.
```python
op = blqs.Op("MOV")

@blqs.build
def my_program():
    op(1, 2)
    op(2, 3)

program = my_program()
print(program)
> prints
> MOV 1, 2
> MOV 2, 3
```
`blqs.Op`s have names, which can be used to identify them, and an `blqs.Op`
can be called on objects to produce a `blqs.Instruction`.  The `blqs.Instruction`
then contains a reference to the `blqs.Op` as well as the objected that `blqs.Op`
was called upon, called the targets.
```
instruction = op(1, 2)
print(instruction.op())
> prints
> MOV
print(instruction.targets())
> prints
> (1, 2)
```
Here our targets were two `int`s but we could use any python object.

One nice property of this separation is that one can create a set of ops that
are canonical for your use case and then use them to construct statements
as necessary depending on different targets.

## Native Statements and Protocols

In addition to constructing statements either directly, or via turning ops
and targets into instructions, one can also use blqs to capture native
python statements.  Here is an example
```python
@blqs.build
def my_program():
    op1 = blqs.Op("A")
    if blqs.Register("a"):
        op1(1)
    else:
        op1(2)
        op1(3)

program = my_program()
print(program)
> prints
> if R(a):
>   A 1
> else:
>   A 2
>   A 3
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
>   A 3
```

Let's compare this to another use of an if statement in blqs program:
```python
@blqs.build
def my_program(x):
    op1 = blqs.Op("A")
    if x:
        op1(1)
    else:
        op1(2)
        op1(3)

program = my_program(True)
print(program)
> prints
> A 1
program = my_program(False)
print(program)
> prints
> A 2
> A 3
```
Here we see that instead of capturing the if statement, it treats the
variable `x` as a normal python variable and the if statement containing
it as a normal if statement conditional on that variable's value.

How does blqs decide when to do this?  Well notice above that we passed
in a blqs object in the first conditional, a `blqs.Register`.  The
important property of this object is that it supports the *is readable*
protocol (Here we are thinking about a register as a something that can
store a value, but we could use this for other objects we create.)  What
does it mean that it supports the *is readable* protocol, it means that
if you look at the `Register` class it has a method `_is_readable_` that
return True or False whether the object is readable.  If an object is
readable, then when blqs encounters it during the build stage, it will
treat this as something that it should capture into a `blqs.If` statement.
Whereas, in contrast, our `x` variable above is just a `bool` which does not
have the `_is_readable_` method.

Classes that implement methods, such as `_is_readable_`, which then allows
these classes to have different behavior are an example of a protocol, also
known as structural subtyping. In structure subtyping an element is considered
of the same type if has the same feature. What this means for us is that
any class that implements `_is_readable_` according to the contract of
the protocol (in this care returning a bool and taking no args), implements
the `SupportsIsReadable` protocol. At runtime this can be used to determine
how this object should be treated. In our case if `_is_readable_` is
implemented, then blqs knows that it should capture the `if` expression,
otherwise it should not.

Blqs in general uses protocols to determine how it should capture
the content of a python program that it is building. For more details,
see the document on [protocols and capturing native python](protocols.md).

## Learn More

* [Intro](intro.md)
* [Protocols and Capturing Native Python](protocols.md)
