"""
Module for carrying and caching results.
"""

from typing import Any, Callable, Dict, Tuple, Optional
from collections import OrderedDict
import functools


def curry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Convert a function of multiple arguments into its curried form.
    
    Currying transforms a function taking N arguments into a sequence of
    functions each taking one argument.
    
    Args:
        function: The function to be curried.
        arity: The number of arguments the function expects.

    Returns:
        A curried version of the function.
    
    Raises:
        TypeError: If arity is negative or not an integer.
        ValueError: If too many arguments are passed to the curried function.
    """
    if not isinstance(arity, int) or arity < 0:
        raise TypeError("Arity must be a non-negative integer")

    if arity == 0:
        def zero_arity_curried() -> Any:
            return function()
        return zero_arity_curried

    def curried(*args: Any) -> Any:
        if len(args) > arity:
            raise ValueError(f"Expected at most {arity} arguments, got {len(args)}")
        if len(args) == arity:
            return function(*args)
        else:
            def next_curried(next_arg: Any) -> Any:
                return curried(*(args + (next_arg,)))
            return next_curried

    return curried


def uncurry_explicit(function: Callable[..., Any], arity: int) -> Callable[..., Any]:
    """
    Convert a curried function back into a regular function.
    
    Args:
        function: The curried function to uncurry.
        arity: The number of arguments the resulting function should accept.

    Returns:
        A regular (uncurried) function.
    
    Raises:
        TypeError: If arity is negative or not an integer.
        ValueError: If the number of provided arguments does not match the arity.
    """
    if not isinstance(arity, int) or arity < 0:
        raise TypeError("Arity must be a non-negative integer")

    if arity == 0:
        def zero_arity_uncurried() -> Any:
            return function()
        return zero_arity_uncurried

    def uncurried(*args: Any) -> Any:
        if len(args) != arity:
            raise ValueError(f"Expected exactly {arity} arguments, got {len(args)}")
        result = function
        for arg in args:
            result = result(arg)
        return result

    return uncurried


def cache(times: Optional[int] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:

    """
    Decorator that caches the results of function calls.
    
    Supports both positional and keyword arguments. If `times` is None, caching is disabled.

    Args:
        times: Number of recent results to cache. Must be a non-negative integer or None.

    Returns:
        A decorator that wraps the function with caching behavior.
    
    Raises:
        ValueError: If `times` is negative or not an integer.
    """
    if times is None:
        def no_cache_decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            @functools.wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)
            return wrapper
        return no_cache_decorator

    if not isinstance(times, int) or times < 0:
        raise ValueError("Cache times must be a non-negative integer")

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache_storage: Dict[Tuple[Tuple[Any, ...], frozenset], Tuple[Any, int]] = OrderedDict()

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = (args, frozenset(kwargs.items()))
            if key in cache_storage:
                result, count = cache_storage[key]
                if count > 1:
                    cache_storage[key] = (result, count - 1)
                else:
                    del cache_storage[key]
                return result

            result = func(*args, **kwargs)
            cache_storage[key] = (result, times)

            if len(cache_storage) > times:
                cache_storage.popitem(last=False)

            return result

        return wrapper

    return decorator
