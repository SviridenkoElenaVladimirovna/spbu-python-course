"""

Tests for the streaming operations module
"""
import pytest
from typing import List, Any, Iterator, Generator, Iterable
from project.task2.generators import (
    stream,
    adapt_operation,
    run_pipeline,
    collect,
    map_stream,
    filter_stream,
    zip_stream,
    reduce_stream,
)


@pytest.fixture
def sample_numbers() -> List[int]:
    """Fixture providing sample integer data for testing."""
    return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


@pytest.fixture
def sample_strings() -> List[str]:
    """Fixture providing sample string data for testing."""
    return ["apple", "banana", "cherry", "date", "elderberry"]


def test_stream_basic(sample_numbers: List[int]) -> None:
    """Test basic stream creation from a list."""
    result = collect(stream(sample_numbers))
    assert result == sample_numbers


def test_stream_empty() -> None:
    """Test stream creation from empty input."""
    result = collect(stream([]))
    assert result == []


@pytest.mark.parametrize(
    "input_data,expected",
    [
        ([1, 2, 3], [1, 2, 3]),
        (range(3), [0, 1, 2]),
        ((x for x in range(3)), [0, 1, 2]),
    ],
)
def test_stream_various_sources(input_data: Iterable, expected: List) -> None:
    """Test stream creation from different data sources."""
    result = collect(stream(input_data))
    assert result == expected


def test_map_stream(sample_numbers: List[int]) -> None:
    """Test map operation on stream data."""
    mapper = map_stream(lambda x: x * 2)
    result = collect(mapper(stream(sample_numbers)))
    expected = [x * 2 for x in sample_numbers]
    assert result == expected


def test_filter_stream(sample_numbers: List[int]) -> None:
    """Test filter operation on stream data."""
    filterer = filter_stream(lambda x: x % 2 == 0)
    result = collect(filterer(stream(sample_numbers)))
    expected = [2, 4, 6, 8, 10]
    assert result == expected


def test_zip_stream() -> None:
    """Test zip operation combining stream with other iterables."""
    zipper = zip_stream(["a", "b", "c"])
    result = collect(zipper(stream([1, 2, 3])))
    expected = [(1, "a"), (2, "b"), (3, "c")]
    assert result == expected


def test_reduce_stream_with_initial(sample_numbers: List[int]) -> None:
    """Test reduce operation with initial value."""
    reducer = reduce_stream(lambda x, y: x + y, 100)
    result = collect(reducer(stream(sample_numbers[:3])))
    expected = [106]
    assert result == expected


def test_reduce_stream_no_initial(sample_numbers: List[int]) -> None:
    """Test reduce operation without initial value."""
    reducer = reduce_stream(lambda x, y: x + y)
    result = collect(reducer(stream(sample_numbers[:3])))
    expected = [6]
    assert result == expected


def test_run_pipeline_single_operation(sample_numbers: List[int]) -> None:
    """Test pipeline with single operation."""
    mapper = map_stream(lambda x: x * 2)
    result_stream = run_pipeline(stream(sample_numbers), mapper)
    result = collect(result_stream)
    expected = [x * 2 for x in sample_numbers]
    assert result == expected


def test_run_pipeline_multiple_operations(sample_numbers: List[int]) -> None:
    """Test pipeline with multiple sequential operations."""
    mapper = map_stream(lambda x: x * 2)
    filterer = filter_stream(lambda x: x > 10)
    result_stream = run_pipeline(stream(sample_numbers), mapper, filterer)
    result = collect(result_stream)
    expected = [12, 14, 16, 18, 20]
    assert result == expected


def test_run_pipeline_complex_sequence(sample_numbers: List[int]) -> None:
    """Test complex sequence of operations in pipeline."""
    map_double = map_stream(lambda x: x * 2)
    filter_even = filter_stream(lambda x: x % 4 == 0)
    map_add_one = map_stream(lambda x: x + 1)

    result_stream = run_pipeline(
        stream(sample_numbers), map_double, filter_even, map_add_one
    )
    result = collect(result_stream)
    expected = [5, 9, 13, 17, 21]
    assert result == expected


def test_collect_to_set() -> None:
    """Test collecting stream results into a set."""
    data = [1, 2, 2, 3, 3, 3]
    result = collect(stream(data), set)
    assert result == {1, 2, 3}


def test_collect_to_tuple(sample_numbers: List[int]) -> None:
    """Test collecting stream results into a tuple."""
    result = collect(stream(sample_numbers[:3]), tuple)
    assert result == (1, 2, 3)


def test_collect_to_dict(sample_strings: List[str]) -> None:
    """Test collecting stream results into a dictionary."""
    enum_op = adapt_operation(enumerate)
    stream_iter = stream(sample_strings[:3])
    processed = enum_op(stream_iter)
    result = collect(processed, dict)
    expected = {0: "apple", 1: "banana", 2: "cherry"}
    assert result == expected


def test_custom_operation(sample_numbers: List[int]) -> None:
    """Test using custom operation with adapt_operation."""

    def custom_multiply(stream_iter: Iterator[int]) -> Generator[int, None, None]:
        for item in stream_iter:
            yield item * 3

    custom_op = adapt_operation(custom_multiply)
    result = collect(custom_op(stream(sample_numbers[:3])))
    expected = [3, 6, 9]
    assert result == expected


def test_lazy_evaluation(sample_numbers: List[int]) -> None:
    """Test that stream processing is lazy (elements processed on-demand)."""
    evaluation_tracker = []

    def tracking_map(x: int) -> int:
        evaluation_tracker.append(x)
        return x * 2

    mapper = map_stream(tracking_map)
    stream_iter = mapper(stream(sample_numbers))

    assert len(evaluation_tracker) == 0

    first_item = next(stream_iter)
    assert first_item == 2
    assert len(evaluation_tracker) == 1
    assert evaluation_tracker == [1]

    second_item = next(stream_iter)
    assert second_item == 4
    assert len(evaluation_tracker) == 2
    assert evaluation_tracker == [1, 2]


def test_empty_stream_through_pipeline() -> None:
    """Test pipeline behavior with empty input stream."""
    mapper = map_stream(lambda x: x * 2)
    filterer = filter_stream(lambda x: x > 10)
    result_stream = run_pipeline(stream([]), mapper, filterer)
    result = collect(result_stream)
    assert result == []


@pytest.mark.parametrize(
    "operations,expected",
    [
        (
            [map_stream(lambda x: x * 3), filter_stream(lambda x: x % 2 == 1)],
            [3, 9, 15],
        ),
        (
            [map_stream(lambda x: x + 10), filter_stream(lambda x: x < 15)],
            [11, 12, 13, 14],
        ),
    ],
)
def test_parametrized_operations(operations: List, expected: List[int]) -> None:
    """Test various operation combinations using parametrized testing."""
    result_stream = run_pipeline(stream([1, 2, 3, 4, 5]), *operations)
    result = collect(result_stream)
    assert result == expected


def test_adapt_operation_with_enumerate(sample_strings: List[str]) -> None:
    """Test adapt_operation with enumerate function."""
    enum_op = adapt_operation(enumerate, start=1)
    result = collect(enum_op(stream(sample_strings[:3])))
    expected = [(1, "apple"), (2, "banana"), (3, "cherry")]
    assert result == expected


def test_zip_stream_multiple_iterables() -> None:
    """Test zip operation with multiple iterables."""
    zipper = zip_stream([10, 20, 30], ["a", "b", "c"])
    result = collect(zipper(stream([1, 2, 3])))
    expected = [(1, 10, "a"), (2, 20, "b"), (3, 30, "c")]
    assert result == expected


def test_pipeline_with_mixed_operations(sample_numbers: List[int]) -> None:
    """Test pipeline combining map, filter, and reduce operations."""
    map_op = map_stream(lambda x: x * 3)
    filter_op = filter_stream(lambda x: x > 10)
    reduce_op = reduce_stream(lambda x, y: x + y)

    result_stream = run_pipeline(
        stream(sample_numbers[:4]), map_op, filter_op, reduce_op
    )
    result = collect(result_stream)
    expected = [12]
    assert result == expected
