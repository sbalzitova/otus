#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import update_wrapper, wraps


def disable(func):
    """
    Disable a decorator by re-assigning the decorator's name
    to this function. For example, to turn off memoization:

    memo = disable

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def decorator(func):
    """
    Decorate a decorator so that it inherits the docstrings
    and stuff from the function it's decorating.
    """
    update_wrapper(decorator, func)
    return func


def countcalls(func):
    """Decorator that counts calls made to the function decorated."""

    @wraps(func)
    def counter(*args, **kwargs):
        counter.calls += 1
        return func(*args, **kwargs)

    counter.calls = 0
    return counter


def memo(func):
    """
    Memoize a function so that it caches all return values for
    faster future lookups.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):

        cache = {}

        key = args

        if kwargs:
            key += tuple(kwargs.items())

        if key not in cache:
            cache[key] = func(*args, **kwargs)

        return cache[key]

    return wrapper


def n_ary(func):
    """
    Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        a = list(args)

        if kwargs:
            a.append(list(kwargs.items()))

        if len(a) == 1:
            return a[0]

        if len(a) == 2:
            return func(*a)

        return wrapper(a[0], wrapper(*a[1:]))

    return wrapper


def trace(symbols):
    """Trace calls made to function decorated.

    @trace("____")
    def fib(n):
        ....

    >>> fib(3)
     --> fib(3)
    ____ --> fib(2)
    ________ --> fib(1)
    ________ <-- fib(1) == 1
    ________ --> fib(0)
    ________ <-- fib(0) == 1
    ____ <-- fib(2) == 2
    ____ --> fib(1)
    ____ <-- fib(1) == 1
     <-- fib(3) == 3

    """

    def real_decorator(func):
        func.cur_indent = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            indent = symbols * func.cur_indent
            arg_str = ''.join(
                [str(a) for a in args] +
                ['{}={}'.format(a, str(b)) for a, b in kwargs.items()])

            print('{}-->{}({})'.format(indent, func.__name__, arg_str))

            func.cur_indent += 1
            returned_value = func(*args, **kwargs)
            func.cur_indent -= 1

            print('{}<--{}({}) == {}'.format(indent, func.__name__, arg_str, returned_value))

            return returned_value
        return wrapper
    return real_decorator


@countcalls
@memo
@n_ary
def foo(a, b):
    return a + b


@countcalls
@memo
@n_ary
def bar(a, b):
    return a * b


@countcalls
@memo
@trace("####")
def fib(n):
    """Some doc"""
    return 1 if n <= 1 else fib(n-1) + fib(n-2)


def main():
    print(foo(4, 3))
    print(foo(4, 3, 2))
    print(foo(4, 3))
    print("foo was called", foo.calls, "times")

    print(bar(4, 3))
    print(bar(4, 3, 2))
    print(bar(4, 3, 2, 1))
    print("bar was called", bar.calls, "times")

    print(fib.__doc__)
    fib(3)
    print(fib.calls, 'calls made')


if __name__ == '__main__':
    main()
