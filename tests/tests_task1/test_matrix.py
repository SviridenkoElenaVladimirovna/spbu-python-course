"""
Test module for matrix operations.
"""

import pytest
import math
from project.task1.matrix import (
    matrix_addition,
    matrix_multiplication,
    matrix_transpose,
)


def test_matrix_addition_basic():
    """Test basic matrix addition."""
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]
    expected = [[6, 8], [10, 12]]
    assert matrix_addition(matrix1, matrix2) == expected


def test_matrix_addition_different_dimensions():
    """Test matrix addition with incompatible dimensions."""
    with pytest.raises(ValueError, match="same dimensions"):
        matrix_addition([[1, 2]], [[1, 2, 3]])


def test_matrix_multiplication_basic():
    """Test basic matrix multiplication."""
    matrix1 = [[1, 2], [3, 4]]
    matrix2 = [[5, 6], [7, 8]]
    expected = [[19, 22], [43, 50]]
    assert matrix_multiplication(matrix1, matrix2) == expected


def test_matrix_multiplication_rectangular():
    """Test multiplication of rectangular matrices."""
    matrix1 = [[1, 2, 3], [4, 5, 6]]
    matrix2 = [[7, 8], [9, 10], [11, 12]]
    expected = [[58, 64], [139, 154]]
    assert matrix_multiplication(matrix1, matrix2) == expected


def test_matrix_multiplication_incompatible_dimensions():
    """Test matrix multiplication with incompatible dimensions."""
    with pytest.raises(ValueError):
        matrix_multiplication([[1, 2]], [[1]])


def test_matrix_transpose_square():
    """Test transposition of square matrix."""
    matrix = [[1, 2], [3, 4]]
    expected = [[1, 3], [2, 4]]
    assert matrix_transpose(matrix) == expected


def test_matrix_transpose_rectangular():
    """Test transposition of rectangular matrix."""
    matrix = [[1, 2, 3], [4, 5, 6]]
    expected = [[1, 4], [2, 5], [3, 6]]
    assert matrix_transpose(matrix) == expected
