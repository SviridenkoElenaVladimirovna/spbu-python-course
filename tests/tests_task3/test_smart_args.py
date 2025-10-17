"""
A set of modular tests for the @smart_args decorator and the Evaluated and Isolated helper classes.
"""

import pytest
import random
from project.task3.smart_args import smart_args, Evaluated, Isolated


def test_isolated_example_from_task():
    """Test the exact Isolated example from the task."""

    @smart_args
    def check_isolation(*, d=Isolated()):
        d["a"] = 0
        return d

    no_mutable = {"a": 10}

    result = check_isolation(d=no_mutable)
    assert result == {"a": 0}
    assert no_mutable == {"a": 10}


def test_evaluated_example_from_task():
    """Test the exact Evaluated example from the task."""
    results = []

    def get_random_number():
        return random.randint(1, 100)

    @smart_args
    def check_evaluation(*, x=Evaluated(lambda: 15), y=Evaluated(get_random_number)):
        results.append((x, y))

    original_randint = random.randint

    random.randint = lambda a, b: 36
    check_evaluation()

    random.randint = lambda a, b: 66
    check_evaluation()

    check_evaluation(y=150)
    random.randint = original_randint

    assert results[0][0] == results[1][0] == results[2][0] == 15

    assert results[0][1] == 36
    assert results[1][1] == 66

    assert results[2][1] == 150


def test_isolated_with_different_types():
    """Test Isolated with various mutable types."""

    @smart_args
    def modify_data(*, data=Isolated()):
        if isinstance(data, list):
            data.append("modified")
        elif isinstance(data, dict):
            data["modified"] = True
        elif isinstance(data, set):
            data.add("modified")
        return data

    original_list = [1, 2, 3]
    result_list = modify_data(data=original_list)
    assert result_list == [1, 2, 3, "modified"]
    assert original_list == [1, 2, 3]

    original_dict = {"a": 1}
    result_dict = modify_data(data=original_dict)
    assert result_dict == {"a": 1, "modified": True}
    assert original_dict == {"a": 1}


def test_evaluated_dynamic_behavior():
    """Test that Evaluated computes new value each time."""
    counter = 0

    def get_incrementing():
        nonlocal counter
        counter += 1
        return counter

    @smart_args
    def test_dynamic(*, value=Evaluated(get_incrementing)):
        return value

    assert test_dynamic() == 1
    assert test_dynamic() == 2
    assert test_dynamic() == 3


def test_evaluated_with_override():
    """Test Evaluated when explicit value is provided."""
    call_count = 0

    def counting_func():
        nonlocal call_count
        call_count += 1
        return call_count

    @smart_args
    def test_override(*, data=Evaluated(counting_func)):
        return data

    assert test_override() == 1
    assert call_count == 1

    assert test_override(data=999) == 999
    assert call_count == 1

    assert test_override() == 2
    assert call_count == 2


def test_isolated_required():
    """Test that Isolated arguments must be provided."""

    @smart_args
    def requires_isolated(*, items=Isolated()):
        return items

    with pytest.raises(ValueError, match="must be explicitly provided"):
        requires_isolated()


def test_positional_arguments_error():
    """Test that positional arguments raise error."""

    @smart_args
    def keyword_only(*, x=Isolated()):
        return x

    with pytest.raises(ValueError, match="keyword arguments only"):
        keyword_only(123)

    result = keyword_only(x=123)
    assert result == 123


def test_regular_keyword_args_still_work():
    """Test that regular keyword arguments work normally."""

    @smart_args
    def regular_func(*, a=1, b=2, c=3):
        return a + b + c

    assert regular_func() == 6
    assert regular_func(a=10) == 15
    assert regular_func(a=1, b=2, c=3) == 6


def test_mixed_arguments():
    """Test mixing regular, Evaluated, and Isolated arguments."""
    eval_calls = 0

    def get_eval():
        nonlocal eval_calls
        eval_calls += 1
        return eval_calls

    @smart_args
    def mixed_function(
        *, regular="default", evaluated=Evaluated(get_eval), isolated=Isolated()
    ):
        return {"regular": regular, "evaluated": evaluated, "isolated": isolated}

    with pytest.raises(ValueError):
        mixed_function()

    result1 = mixed_function(isolated=[1, 2, 3])
    assert result1["regular"] == "default"
    assert result1["evaluated"] == 1
    assert result1["isolated"] == [1, 2, 3]

    result2 = mixed_function(isolated={"a": 1})
    assert result2["evaluated"] == 2

    result3 = mixed_function(regular="custom", evaluated=100, isolated=[])
    assert result3["regular"] == "custom"
    assert result3["evaluated"] == 100
    assert result3["isolated"] == []


def test_invalid_evaluated_function():
    """Test that Evaluated with function that takes arguments fails."""

    def func_with_args(x):
        return x

    with pytest.raises(AssertionError, match="must take no arguments"):
        Evaluated(func_with_args)


def test_deep_copy_effectiveness():
    """Test that Isolated really creates independent copies."""
    original = {"list": [1, 2, 3], "dict": {"nested": "value"}, "set": {1, 2, 3}}

    @smart_args
    def deeply_modify(*, data=Isolated()):
        data["list"].append(4)
        data["dict"]["new"] = "item"
        data["set"].add(4)
        data["new_key"] = "value"
        return data

    result = deeply_modify(data=original)

    assert 4 in result["list"]
    assert "new" in result["dict"]
    assert 4 in result["set"]
    assert "new_key" in result

    assert 4 not in original["list"]
    assert "new" not in original["dict"]
    assert 4 not in original["set"]
    assert "new_key" not in original


def test_complex_scenario():
    """Test complex scenario with multiple decorated functions."""

    @smart_args
    def func1(*, counter=1, data=Isolated()):
        data["processed"] = True
        return counter, data

    @smart_args
    def func2(*, items=Isolated()):
        items.sort()
        return items

    result1 = func1(data={"value": 1})
    assert result1[0] == 1
    assert result1[1] == {"value": 1, "processed": True}

    result2 = func1(data={"value": 2})
    assert result2[0] == 1
    assert result2[1] == {"value": 2, "processed": True}

    original_list = [3, 1, 2]
    result3 = func2(items=original_list)
    assert result3 == [1, 2, 3]
    assert original_list == [3, 1, 2]


def test_evaluated_with_method():
    """Test Evaluated with class methods."""

    class Counter:
        def __init__(self):
            self.count = 0

        def get_count(self):
            self.count += 1
            return self.count

    counter = Counter()

    @smart_args
    def test_method(*, value=Evaluated(counter.get_count)):
        return value

    assert test_method() == 1
    assert test_method() == 2
    assert test_method() == 3


def test_multiple_evaluated_arguments():
    """Test multiple Evaluated arguments in same function."""
    counter1 = 0
    counter2 = 0

    def get_counter1():
        nonlocal counter1
        counter1 += 1
        return counter1

    def get_counter2():
        nonlocal counter2
        counter2 += 1
        return counter2 * 10

    @smart_args
    def multiple_evaluated(*, a=Evaluated(get_counter1), b=Evaluated(get_counter2)):
        return a, b

    result1 = multiple_evaluated()
    assert result1 == (1, 10)

    result2 = multiple_evaluated()
    assert result2 == (2, 20)

    result3 = multiple_evaluated(a=100)
    assert result3 == (100, 30)


def test_positional_arguments_not_allowed():
    """Test that positional arguments are not allowed in basic mode."""
    with pytest.raises(AssertionError):

        @smart_args
        def invalid_func(a=Evaluated(lambda: 1)):
            pass

    with pytest.raises(AssertionError):

        @smart_args
        def invalid_func2(a=Isolated()):
            pass


def test_keyword_only_enforcement():
    """Test that functions must use keyword-only arguments."""
    with pytest.raises(AssertionError):

        @smart_args
        def invalid_func(a, b):
            pass


def test_smart_args_without_parameters():
    """Test that @smart_args without parameters works."""

    @smart_args
    def func(*, x=Evaluated(lambda: 1), y=Isolated()):
        return x, y

    result = func(y=[1, 2])
    assert result == (1, [1, 2])

    with pytest.raises(ValueError):
        func()
