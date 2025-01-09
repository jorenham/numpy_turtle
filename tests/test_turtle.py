import math

import numpy as np
import numpy.typing as npt
import pytest

from numpy_turtle import Turtle


@pytest.fixture
def canvas() -> npt.NDArray[np.uint8]:
    return np.zeros((10, 10, 3), dtype=np.uint8)


@pytest.fixture
def turtle(canvas: npt.NDArray[np.uint8]) -> Turtle[np.uint8]:
    """Turtle on an array"""
    return Turtle(canvas)


def test_pos_forward(turtle: Turtle[np.uint8]) -> None:
    turtle.forward(1)
    turtle.forward(1)
    assert turtle.position == (2, 0)


def test_pos_forward_out_of_bounds(turtle: Turtle[np.uint8]) -> None:
    turtle.forward(10)
    turtle.forward(10)
    assert turtle.position == (20, 0)


def test_full_square(turtle: Turtle[np.uint8]) -> None:
    for _ in range(4):
        turtle.forward(10)
        turtle.rotate(0.5 * np.pi)

    expected = np.zeros_like(turtle.array)
    expected[:, :] = turtle.color
    expected[1:-1, 1:-1, :] = 0

    np.testing.assert_array_equal(turtle.array, expected)


def test_eye(turtle: Turtle[np.uint8]) -> None:
    size = turtle.array.shape[0]

    turtle.rotate(0.25 * np.pi)
    turtle.forward(math.sqrt(2) * size)

    eye = np.eye(size, dtype=turtle.array.dtype)
    eye3 = np.zeros_like(turtle.array)
    for i, c in enumerate(np.array(turtle.color)):  # pyright: ignore[reportAny]
        eye3[:, :, i] = eye * c

    np.testing.assert_array_equal(turtle.array, eye3)
