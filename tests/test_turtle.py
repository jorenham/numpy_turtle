import numpy as np
import numpy.testing as npt

import pytest as pytest

from numpy_turtle import Turtle


@pytest.fixture
def canvas():
    """A 2-dimensional 10x10 RGB24 image"""
    return np.zeros((10, 10, 3), dtype=np.uint8)


@pytest.fixture
def turtle(canvas):
    """Turtle on an array"""
    return Turtle(canvas)


def test_pos_forward(turtle):
    turtle.forward(1)
    turtle.forward(1)
    assert turtle.position == (2, 0)


def test_pos_forward_out_of_bounds(turtle):
    turtle.forward(10)
    turtle.forward(10)
    assert turtle.position == (20, 0)


def test_full_square(turtle):
    for _ in range(4):
        turtle.forward(10)
        turtle.rotate(0.5 * np.pi)

    expected = np.zeros_like(turtle.array)
    expected[:, :] = turtle.color
    expected[1:-1, 1:-1, :] = 0

    npt.assert_array_equal(turtle.array, expected)


def test_eye(turtle):
    size = turtle.array.shape[0]

    turtle.rotate(0.25 * np.pi)
    turtle.forward(np.sqrt(2) * size)

    eye = np.eye(size, dtype=turtle.array.dtype)
    eye3 = np.zeros_like(turtle.array)
    for i, c in enumerate(turtle.color):
        eye3[:, :, i] = eye * c

    npt.assert_array_equal(turtle.array, eye3)
