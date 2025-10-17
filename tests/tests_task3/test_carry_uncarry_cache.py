"""
A set of unit tests for the curry_explicit, uncurry_explicit functions, and the cache decorator.
"""

import pytest
import time
from project.task3.carry_uncarry_cache import curry_explicit, uncurry_explicit, cache


def test_curry_basic():
    """Test basic currying and uncurrying behavior."""
    f2 = curry_explicit((lambda x, y, z: f"<{x},{y},{z}>"), 3)
    g2 = uncurry_explicit(f2, 3)

    assert f2(123)(456)(562) == "<123,456,562>"
    assert g2(123, 456, 562) == "<123,456,562>"


def test_curry_arity_zero():
    """Test currying with arity 0."""
    f0 = curry_explicit(lambda: "zero", 0)
    assert f0() == "zero"


def test_curry_arity_one():
    """Test currying with arity 1."""
    f1 = curry_explicit(lambda x: f"<{x}>", 1)
    assert f1(42) == "<42>"


def test_uncurry_basic():
    """Test basic uncurrying functionality."""
    f0 = curry_explicit(lambda: "zero", 0)
    g0 = uncurry_explicit(f0, 0)
    assert g0() == "zero"

    f1 = curry_explicit(lambda x: f"<{x}>", 1)
    g1 = uncurry_explicit(f1, 1)
    assert g1(42) == "<42>"


def test_curry_negative_arity():
    """Test that negative arity raises TypeError."""
    with pytest.raises(TypeError):
        curry_explicit(lambda x: x, -1)


def test_uncurry_negative_arity():
    """Test that negative arity raises TypeError for uncurry."""
    with pytest.raises(TypeError):
        uncurry_explicit(lambda x: x, -1)


def test_curry_non_integer_arity():
    """Test that non-integer arity raises TypeError."""
    with pytest.raises(TypeError):
        curry_explicit(lambda x: x, "2")


def test_uncurry_non_integer_arity():
    """Test that non-integer arity raises TypeError for uncurry."""
    with pytest.raises(TypeError):
        uncurry_explicit(lambda x: x, 2.5)


def test_curry_too_many_arguments():
    """Test that too many arguments in one call raises ValueError."""
    f2 = curry_explicit((lambda x, y: x + y), 2)
    with pytest.raises(ValueError):
        f2(1, 2, 3)


def test_curry_too_many_nested_calls():
    """Test that too many arguments in nested calls raises appropriate error."""
    f2 = curry_explicit((lambda x, y: x + y), 2)
    result = f2(1)(2)
    with pytest.raises(TypeError):
        result(3)


def test_uncurry_wrong_argument_count():
    """Test that wrong number of arguments raises ValueError for uncurry."""
    f2 = curry_explicit((lambda x, y: x + y), 2)
    g2 = uncurry_explicit(f2, 2)

    with pytest.raises(ValueError):
        g2(1)

    with pytest.raises(ValueError):
        g2(1, 2, 3)


def test_strict_currying():
    """Test strict currying with one argument per call."""
    f3 = curry_explicit((lambda a, b, c: a + b + c), 3)
    assert f3(1)(2)(3) == 6


def test_curry_partial_application():
    """Test partial application with currying."""
    f3 = curry_explicit((lambda a, b, c: a * b * c), 3)
    f_partial = f3(2)
    f_more_partial = f_partial(3)
    assert f_more_partial(4) == 24


def test_curry_with_different_functions():
    """Test currying with various function types."""
    f_concat = curry_explicit((lambda a, b: a + b), 2)
    assert f_concat("hello")(" world") == "hello world"

    f_power = curry_explicit((lambda x, y: x**y), 2)
    assert f_power(2)(3) == 8


def test_uncurry_preserves_behavior():
    """Test that uncurry preserves the original function behavior."""
    original = lambda x, y, z: (x + y) * z
    curried = curry_explicit(original, 3)
    uncurried = uncurry_explicit(curried, 3)

    assert original(1, 2, 3) == uncurried(1, 2, 3) == 9


def test_curry_uncurry_round_trip():
    """Test that curry and uncurry are inverse operations."""
    original = lambda a, b, c, d: a + b * c - d
    curried = curry_explicit(original, 4)
    uncurried = uncurry_explicit(curried, 4)

    test_args = (5, 3, 2, 1)
    assert original(*test_args) == uncurried(*test_args) == 10


def test_curry_zero_arity_multiple_calls():
    """Test that zero-arity function can be called multiple times."""
    counter = 0

    def counter_func():
        nonlocal counter
        counter += 1
        return counter

    f0 = curry_explicit(counter_func, 0)
    assert f0() == 1
    assert f0() == 2
    assert f0() == 3


def test_curry_single_argument_multiple_times():
    """Test currying with single argument function called multiple times."""
    f1 = curry_explicit(lambda x: x * 2, 1)
    assert f1(5) == 10
    assert f1(10) == 20
    assert f1(0) == 0


def test_curry_with_print_function():
    """Test currying with print function (arbitrary arity function)."""
    curried_print = curry_explicit(print, 2)
    result = curried_print("Hello")("World")
    assert result is None
    with pytest.raises(TypeError):
        result("extra")


def test_curry_edge_cases():
    """Test edge cases for currying."""
    f0 = curry_explicit(lambda: 42, 0)
    assert f0() == 42

    f1 = curry_explicit(lambda x: x, 1)
    assert f1(100) == 100


def test_cache_basic():
    """Test basic caching functionality."""
    call_count = 0

    @cache(times=2)
    def test_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    assert test_func(5) == 10
    assert call_count == 1

    assert test_func(5) == 10
    assert call_count == 1

    assert test_func(5) == 10
    assert call_count == 1


def test_cache_different_arguments():
    """Test caching with different arguments."""
    call_count = 0

    @cache(times=3)
    def test_func(x, y=0):
        nonlocal call_count
        call_count += 1
        return x + y

    assert test_func(1) == 1
    assert call_count == 1

    assert test_func(2) == 2
    assert call_count == 2

    assert test_func(1, 1) == 2
    assert call_count == 3

    assert test_func(1) == 1
    assert call_count == 3


def test_cache_with_kwargs():
    """Test caching with keyword arguments."""
    call_count = 0

    @cache(times=2)
    def test_func(a, b=0, c=0):
        nonlocal call_count
        call_count += 1
        return a + b + c

    assert test_func(1, 2, 3) == 6
    assert call_count == 1

    assert test_func(1, b=2, c=3) == 6
    assert call_count == 2

    assert test_func(a=1, b=2, c=3) == 6
    assert call_count == 3


def test_cache_expiration():
    """Test that cache entries expire after specified times."""
    call_count = 0

    @cache(times=1)
    def test_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    assert test_func(5) == 10
    assert call_count == 1

    assert test_func(5) == 10
    assert call_count == 1

    assert test_func(5) == 10
    assert call_count == 2


def test_cache_size_limit():
    """Test that cache respects size limits."""
    call_count = 0

    @cache(times=2)
    def test_func(x):
        nonlocal call_count
        call_count += 1
        return x

    assert test_func(1) == 1
    assert test_func(2) == 2
    assert call_count == 2

    assert test_func(3) == 3
    assert call_count == 3

    assert test_func(1) == 1
    assert call_count == 4


def test_no_cache():
    """Test behavior when cache is disabled (times=None)."""
    call_count = 0

    @cache(times=None)
    def test_func(x):
        nonlocal call_count
        call_count += 1
        return x * 2

    assert test_func(5) == 10
    assert call_count == 1

    assert test_func(5) == 10
    assert call_count == 2


def test_cache_with_complex_arguments():
    """Test caching with complex argument types."""

    @cache(times=2)
    def test_func(*args, **kwargs):
        return (args, kwargs)

    result1 = test_func(1, 2, a=3, b=4)
    result2 = test_func(1, 2, a=3, b=4)

    assert result1 == result2
    assert result1 == ((1, 2), {"a": 3, "b": 4})


def test_cache_performance():
    """Test that caching improves performance for expensive functions."""
    call_count = 0

    @cache(times=2)
    def expensive_func(x):
        nonlocal call_count
        call_count += 1
        time.sleep(0.01)
        return x * 2

    start_time = time.time()

    expensive_func(5)
    first_call_time = time.time() - start_time

    start_time = time.time()
    expensive_func(5)
    second_call_time = time.time() - start_time

    assert second_call_time < first_call_time / 2
    assert call_count == 1


def test_cache_error_cases():
    """Test error handling in cache decorator."""
    with pytest.raises(ValueError):

        @cache(times=-1)
        def test_func(x):
            return x

    with pytest.raises(ValueError):

        @cache(times="invalid")
        def test_func(x):
            return x
