"""
Lazy Stream Framework

This module implements a lazy data stream framework using Python generators.
"""

from typing import Iterable, Callable, Iterator, Any
from functools import reduce


def stream(source: Iterable[Any]) -> Iterator[Any]:
    """
    Lazily yield items from the input iterable.

    Args:
        source (Iterable[Any]): Input data source

    Returns:
        Iterator[Any]: Lazy iterator over the input data
    """
    for item in source:
        yield item


def adapt_operation(func: Callable, *args: Any, **kwargs: Any) -> Callable[[Iterator[Any]], Iterator[Any]]:
    """
    Wrap a function to make it compatible with the lazy stream pipeline.

    Supports built-in functions like map, filter, zip, reduce, enumerate,
    as well as custom user-defined functions.

    Args:
        func (Callable): Function to adapt
        *args: Positional arguments for the function
        **kwargs: Keyword arguments for the function

    Returns:
        Callable[[Iterator[Any]], Iterator[Any]]: Adapted operation
    """
    def operation(stream_iter: Iterator[Any]) -> Iterator[Any]:
        if func is map:
            yield from map(args[0], stream_iter)
        elif func is filter:
            yield from filter(args[0], stream_iter)
        elif func is zip:
            yield from zip(stream_iter, *args)
        elif func is enumerate:
            yield from enumerate(stream_iter, *args, **kwargs)
        elif func is reduce:
            reducer=args[0]
            if len(args)>1:
                result = reduce(reducer,stream_iter,args[1])
            elif "initial" in kwargs:
                result = reduce(reducer,stream_iter,kwargs["initial"])
            else:
                result=reduce(reducer,stream_iter)
            yield result
        else:
            yield from func(stream_iter, *args, **kwargs)
    return operation


def run_pipeline(stream_iter: Iterator[Any], *operations: Callable[[Iterator[Any]], Iterator[Any]]) -> Iterator[Any]:
    """
    Apply a sequence of operations to the stream lazily.

    Args:
        stream_iter (Iterator[Any]): Input data stream
        *operations: Operations to apply sequentially

    Returns:
        Iterator[Any]: Stream after all operations
    """
    current = stream_iter
    for op in operations:
        current = op(current)
    return current


def collect(stream_iter: Iterator[Any], collector: Callable[..., Any] = list, *args: Any, **kwargs: Any) -> Any:
    """
    Collect items from a stream into a specified collection type.

    Args:
        stream_iter (Iterator[Any]): Processed stream
        collector (Callable): Factory for collection (list, set, tuple, etc.)
        *args, **kwargs: Arguments for collector

    Returns:
        Any: Collected data
    """
    return collector(stream_iter, *args, **kwargs)


def map_stream(func: Callable[[Any], Any]) -> Callable[[Iterator[Any]], Iterator[Any]]:
    """
    Create a map operation for the stream pipeline.

    Args:
        func (Callable[[Any], Any]): Function to apply to each element

    Returns:
        Callable[[Iterator[Any]], Iterator[Any]]: Stream map operation
    """
    return adapt_operation(map, func)


def filter_stream(predicate: Callable[[Any], bool]) -> Callable[[Iterator[Any]], Iterator[Any]]:
    """
    Create a filter operation for the stream pipeline.

    Args:
        predicate (Callable[[Any], bool]): Filter predicate function

    Returns:
        Callable[[Iterator[Any]], Iterator[Any]]: Stream filter operation
    """
    return adapt_operation(filter, predicate)


def zip_stream(*others: Iterable[Any]) -> Callable[[Iterator[Any]], Iterator[Any]]:
    """
    Create a zip operation for the stream pipeline.

    Args:
        *others (Iterable[Any]): Other iterables to zip with

    Returns:
        Callable[[Iterator[Any]], Iterator[Any]]: Stream zip operation
    """
    return adapt_operation(zip, *others)


def enumerate_stream(*args: Any, **kwargs: Any) -> Callable[[Iterator[Any]], Iterator[Any]]:
    """
    Create an enumerate operation for the stream pipeline.

    Args:
        *args, **kwargs: Arguments for enumerate

    Returns:
        Callable[[Iterator[Any]], Iterator[Any]]: Stream enumerate operation
    """
    return adapt_operation(enumerate, *args, **kwargs)


def reduce_stream(func: Callable[[Any, Any], Any], initial: Any = None) -> Callable[[Iterator[Any]], Iterator[Any]]:
    """
    Create a reduce operation for the stream pipeline.

    Args:
        func (Callable[[Any, Any], Any]): Reduce function
        initial (Any, optional): Initial value for reduction

    Returns:
        Callable[[Iterator[Any]], Iterator[Any]]: Stream reduce operation
    """
    return adapt_operation(reduce, func, initial)