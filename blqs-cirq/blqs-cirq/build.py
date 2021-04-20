import blqs
import functools


def build(func):
    # @functools.wraps(func)
    # def wrapper(*args, **kwargs):
    #     return func(*args, **kwargs)

    return blqs.build(func)
