#!/usr/bin/env python

from autoexec import execute_function, execute_functions


def add(a: int, b, c=5, d=7., e=None):
    """Some cool addition.

    It's super complicated.
    You know, adding and stuff.

    Parameters
    ----------
    a : int
        This is the first complicated parameter
        super complicated
    b : int, optional
    e : int, optional
    """
    if e is None:
        e = 0
    return a + b + c + d + e


def subtract(a: int, b, c=5, d=7., e=None):
    """Some cool subtraction.

    Parameters
    ----------
    a : int
        This is the first complicated parameter
        super complicated
    b : int, optional
    e : int, optional
    """
    if e is None:
        e = 0
    return a - b - c - d - e


if __name__ == '__main__':
    print(execute_functions([add, subtract]))
    # print(execute_function(add))
