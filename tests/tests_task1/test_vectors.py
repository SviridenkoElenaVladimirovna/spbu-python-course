"""
Test module for vector operations.
"""

import pytest
import math
from project.task1.vectors import dot_product, vector_length, angle_between_vectors


def test_dot_product_basic_cases():
    """Test dot product with basic input vectors."""
    assert dot_product([1, 2, 3], [4, 5, 6]) == 32
    assert dot_product([0, 0], [1, 1]) == 0
    assert dot_product([-1, 2], [3, -4]) == -11


def test_dot_product_different_dimensions():
    """Test dot product with vectors of different dimensions."""
    with pytest.raises(ValueError, match="same dimensions"):
        dot_product([1, 2], [1, 2, 3])


def test_vector_length_calculation():
    """Test vector length calculation."""
    assert vector_length([3, 4]) == 5.0
    assert vector_length([0, 0]) == 0.0
    assert vector_length([1, 1, 1]) == math.sqrt(3)
    assert vector_length([-3, -4]) == 5.0


def test_angle_between_vectors_right_angle():
    """Test angle calculation for perpendicular vectors."""
    angle = angle_between_vectors([1, 0], [0, 1])
    assert math.isclose(angle, math.pi / 2)


def test_angle_between_vectors_same_direction():
    """Test angle calculation for parallel vectors."""
    angle = angle_between_vectors([1, 0], [2, 0])
    assert math.isclose(angle, 0.0)


def test_angle_between_vectors_45_degrees():
    """Test angle calculation for 45-degree case."""
    angle = angle_between_vectors([1, 0], [1, 1])
    assert math.isclose(angle, math.pi / 4)


def test_angle_between_vectors_zero_length():
    """Test angle calculation with zero-length vectors."""
    with pytest.raises(ValueError, match="zero-length"):
        angle_between_vectors([0, 0], [1, 1])
