
# blqs: Quantum Building Blocks

The idea here is to explore a simple framework for supporting data flow like languages in
idiomatic Python.  The inspiration for this is the autograph functionality of TensorFlow 2.0.

For example one should be able to write
```python
import blqs

@blqs.compile
def my_graph():
    # An instruction to allocate memory.
    # In the dataflow graph this is a node that produces and outgoing edge.
    q0 = Alloc(1);
    # An instruction that acts on this memory, in this case it takes an incoming
    # edge from the Alloc above and produces a new output edge corresponding to
    # the memory after applying the gate.
    Gate(q0);
    # Another instruction that acts on this memory, in this case it returns
    # a different type of memory, this will have one incoming edge and two
    # outgoing edges.
    a = Measure(q0);
    # Conditionals in a dataflow graph are typically a condition, plus the
    # True and False branches. Normally this needs to be written with a
    # custom instruction, since `if` cannot be overloaded in Python.
    # We see here we can use idiomatic python to deal with these cases.
    if a > 20:
        Instruction3();
    # This needs to operate seemlessly for cases where we are mixing python
    # natives: for example here the values are used during the construction
    # of the graph, and are depending on the value of the variable the
    # graph that is constructed is different (here the instruction is added).
    b = 3
    if b > 2:
        Instruction4()
    # We can also return the result of an operation, this will be accessible
    # as the output of the dataflow graph.
    return Instruction4();

# Instead of running this function, the annotation `blqs.compile` makes
# the function compile and returns the dataflow graph.
data_flow_graph = my_graph()

# The graph can then be executed or serialized or translated to another
# representation.
run(data_flow_graph)
```

### TODO

Dataflow graph components:
* Block stacks and registering.
* Conditionals.
* For and while loops.
* Exceptions.

AST compiling:
* Block stacks.
* Conditionals.
* For and while loops.
* Exceptions.
