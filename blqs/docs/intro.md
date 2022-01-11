# Introduction to Blqs

Blqs is a library for helping one write imperative domain specific languages in Python.
This means that you can write programs in your own domain specific language in your
Python code, and this program can then be consumed and used by other Python code.
An example of this pattern, and an inspiration for Blqs, can be found in
TensorFlow's [autograph](https://arxiv.org/abs/1810.08061). TensorFlow autograph
allows one to write TensorFlow graphs in an imperative manner, and then autograph
is responsible for turning these into the actual TensorFlow graphs.

Behind the scenes Blqs uses introspection of Python's representation of programs,
its abstract syntax tree, combined with code generation.  You don't really need
to know what this means, but one of the fun parts of writing Blqs was getting
it to work without have to do any static analysis of the Python code (which,
because Python is dynamically typed, is rather hard and messy).  In many ways
Blqs is just a variation of Python's abstract syntax tree, but hopefully it
can be used to avoid the complexity of dealing with the full AST.

## Simple Example

Let's suppose we are building a simple game in which players and non-player
characters (NPCs) live on a square grid.  We'd like to be able to design simple
programs for our NPCs to follow, let's do this as a domain specific language.
For example, you might want your NPC to be able to move in different cardinal
directions. So we can define an op "MOV".
```python
import blqs

mov = blqs.Op("MOV")
```
We can then write a simple program to move in a square, using the `blqs.build`
decorator to indicate this program should be interpreted as our domain
specific language.
```python
@blqs.build
def square_walk():
    mov("N")
    mov("E")
    mov("S")
    mov("W")
```
When we call this method, we get a `blqs.Program` object that contains the
statements describing the walk
```python
program = square_walk()
print(type(program))
> prints
> <class 'blqs.program.Program'>
print(program)
> prints
> MOV N
> MOV E
> MOV S
> MOV W
```
Just moving around is good exercise, but we also want our NPCs to react to their
environment. For example, we might want them to be able to look and see if there is
a barrier in some direction and if not move in that direction
```python
is_empty = blqs.Op("IS_EMPTY")

@blqs.build
def walk():
    x = blqs.Register('X')
    is_empty("N", x)
    if x:
        mov("N")
program = walk()
print(walk())
> prints
> x = R(X)
> IS_EMPTY N,R(X)
> if R(X):
>   MOV N
```
Notice here that we have used Python's native `if` to construct this code. Blqs
notices that the `blqs.Register` method supports a specific protocol, and because
of this it captures that `if` statement and subsequent block into a `blqs.If`
objects
```python
for s in program:
    print(s)
> prints
> <blqs.assignment.Assign object at 0x11130e0a0>
> <blqs.instruction.Instruction object at 0x11130e490>
> <blqs.conditional.If object at 0x11130e1c0>
```
Here we also see that the assignment has been captured.  This `blqs.Program`
object can then be consumed by other Python code, i.e. an executor of these
NPC agents in your game.

## Learn More

* [Concepts](concepts.md)
* [Protocols and Capturing Native Python](protocols.md)

## What Blqs Isn't

* Blqs supports creating languages that very much mimic Python. If you are thinking
of wildly deviating from what a Python program is, blqs probably isn't for you. This
distinction is often said to be between internal domains specific languages (which is
what blqs supports) and external domain specific languages, where one usually writes
a full programming language.
