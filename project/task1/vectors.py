"""
Module for working with vectors
Contains operations:
- scalar product
- vector length
- angle between vectors
"""

import math
from typing import List


def dot_product(vector1: List[float], vector2: List[float]) -> float:
    """Calculate dot product of two vectors.

    Args:
        vector1 (List[float]): First vector.
        vector2 (List[float]): Second vector.

    Returns:
        float: Scalar (dot) product of the vectors.

    Raises:
        ValueError: If vectors have different dimensions.
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have same dimensions")

    return sum(v1 * v2 for v1, v2 in zip(vector1, vector2))


def vector_length(vector: List[float]) -> float:
    """Calculate length of a vector.

    Args:
        vector (List[float]): Input vector.

    Returns:
        float: Euclidean length (magnitude) of the vector.
    """
    return math.sqrt(sum(x * x for x in vector))


def angle_between_vectors(vector1: List[float], vector2: List[float]) -> float:
    """Calculate angle between two vectors in radians.

    Args:
        vector1 (List[float]): First vector.
        vector2 (List[float]): Second vector.

    Returns:
        float: Angle between the vectors in radians.

    Raises:
        ValueError: If vectors have different dimensions.
        ValueError: If any vector has zero length.
    """
    if len(vector1) != len(vector2):
        raise ValueError("Vectors must have same dimensions")

    scalar = dot_product(vector1, vector2)
    len1 = vector_length(vector1)
    len2 = vector_length(vector2)

    if len1 == 0 or len2 == 0:
        raise ValueError("Vectors cannot be zero-length")

    cos_angle = scalar / (len1 * len2)
    cos_angle = max(-1.0, min(1.0, cos_angle))

    return math.acos(cos_angle)
