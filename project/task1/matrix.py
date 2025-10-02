"""
Module for working with matrices
Contains operations:
- matrix addition
- matrix multiplication
- matrix transposition
"""
from typing import List


def matrix_addition(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:
    """Add two matrices."""
    if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
        raise ValueError("Matrices must have same dimensions")

    return [
        [matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))]
        for i in range(len(matrix1))
    ]


def matrix_multiplication(
    matrix1: List[List[float]], matrix2: List[List[float]]
) -> List[List[float]]:
    """Multiply two matrices."""
    if len(matrix1[0]) != len(matrix2):
        raise ValueError(
            "Number of columns in first matrix must equal number of rows in second matrix"
        )

    result = [[0.0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix1))]

    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            for k in range(len(matrix2)):
                result[i][j] += matrix1[i][k] * matrix2[k][j]

    return result


def matrix_transpose(matrix: List[List[float]]) -> List[List[float]]:
    """Transpose a matrix."""
    return [[float(matrix[i][j]) for i in range(len(matrix))] for j in range(len(matrix[0]))]
