import blqs
import cirq
import functools


def build(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        blqs_func = blqs.build(func)
        program = blqs_func(*args, **kwargs)
        circuit = cirq.Circuit()
        for statement in program:
            cirq_op = statement.op().gate().on(*statement.targets())
            circuit.append(cirq_op)
        return circuit

    return wrapper
