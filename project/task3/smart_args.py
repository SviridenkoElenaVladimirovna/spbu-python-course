"""

The module implements the @smart_args decorator and the auxiliary classes Evaluated and Isolated.
"""

import copy
import inspect
import types
from functools import wraps
from typing import Any, Callable


class Evaluated:
    """
    A wrapper for dynamically evaluated default values.
    
    This class is used to mark that a default value should be computed
    at call time by invoking the provided callable.
    
    Args:
        func: A callable that takes no arguments and returns the default value.
    
    Raises:
        AssertionError: If the provided object is not callable or takes arguments.
    """
    
    def __init__(self, func: Callable[[], Any]):
        assert callable(func), "Evaluated must receive a callable object"
        
        if isinstance(func, types.MethodType):
            pass
        elif hasattr(func, '__code__'):
            code = func.__code__
            arg_count = code.co_argcount
            if code.co_flags & 0x04: 
                arg_count -= 1
            if code.co_flags & 0x08:  
                arg_count -= 1
                
            if arg_count > 0:
                raise AssertionError("Function for Evaluated must take no arguments")
        
        self.func = func

    def __call__(self) -> Any:
        """
        Compute the default value by calling the wrapped function.
        
        Returns:
            The result of calling the wrapped function.
        """
        return self.func()


class Isolated:
    """
    A marker for arguments that should be deep-copied when provided explicitly.
    
    When an argument is marked with Isolated(), it must be explicitly provided
    at call time, and the provided value will be deep-copied before being passed
    to the function to prevent mutation of the original object.
    """
    pass


def smart_args(func: Callable) -> Callable:
    """
    A decorator that handles Evaluated and Isolated keyword-only arguments.
    
    This decorator provides advanced handling of default values:
    - Evaluated: Default values are computed at call time
    - Isolated: Arguments are deep-copied when provided explicitly
    
    Args:
        func: The function to be decorated. Must use keyword-only arguments.
    
    Returns:
        The decorated function with smart argument handling.
    
    Raises:
        AssertionError: If the function has non-keyword-only arguments.
        ValueError: If positional arguments are provided or Isolated arguments are missing.
    """
    sig = inspect.signature(func)

    for name, param in sig.parameters.items():
        if param.kind not in (param.KEYWORD_ONLY,):
            raise AssertionError(
                f"Argument '{name}' must be keyword-only. "
                f"Use '*,' to specify keyword-only arguments."
            )

    evaluated_params = []
    isolated_params = []
    
    for name, param in sig.parameters.items():
        default = param.default
        
        if isinstance(default, Evaluated) and isinstance(default, Isolated):
            raise AssertionError(f"Argument '{name}' cannot use both Evaluated and Isolated")

        if isinstance(default, Evaluated):
            evaluated_params.append(name)
        elif isinstance(default, Isolated):
            isolated_params.append(name)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Wrapper function that handles smart argument processing.
        
        Args:
            *args: Positional arguments (not allowed).
            **kwargs: Keyword arguments for the decorated function.
        
        Returns:
            The result of calling the original function with processed arguments.
        
        Raises:
            ValueError: If positional arguments are provided or required Isolated 
                       arguments are missing.
        """
        if args:
            raise ValueError("Function with @smart_args must be called with keyword arguments only")

        for name in isolated_params:
            if name not in kwargs:
                raise ValueError(f"Argument '{name}' with Isolated() must be explicitly provided")

        final_kwargs = {}
        
        for name, param in sig.parameters.items():
            if name in kwargs:
                value = kwargs[name]
                if name in isolated_params:
                    value = copy.deepcopy(value)
                final_kwargs[name] = value
            else:
                default = param.default
                if name in evaluated_params:
                    final_kwargs[name] = default() 
                elif name in isolated_params:
                    raise ValueError(f"Argument '{name}' with Isolated() must be explicitly provided")
                else:
                    final_kwargs[name] = default

        return func(**final_kwargs)

    return wrapper