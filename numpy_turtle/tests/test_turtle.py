from unittest import TestCase

import numpy as np
import numpy.testing as npt

from numpy_turtle import Turtle


class TestTurtleUint8(TestCase):
    def setUp(self):
        self.size = 10
        self.array = np.zeros((self.size, self.size), dtype=np.uint8)
        self.turtle = Turtle(self.array)

    def test_pos_forward(self):
        self.turtle.forward(1)
        self.turtle.forward(1)
        self.assertTupleEqual(self.turtle.position, (2, 0))

    def test_pos_forward_out_of_bounds(self):
        self.turtle.forward(10)
        self.turtle.forward(10)
        self.assertTupleEqual(self.turtle.position, (20, 0))

    def test_full_square(self):
        for _ in range(4):
            self.turtle.forward(10)
            self.turtle.rotate(0.5 * np.pi)

        full_square = np.zeros(self.array.shape, self.array.dtype)
        full_square[0:self.size, 0] = self.turtle.color
        full_square[0:self.size, self.size - 1] = self.turtle.color
        full_square[0, 0:self.size] = self.turtle.color
        full_square[self.size - 1, 0:self.size] = self.turtle.color

        npt.assert_array_equal(self.array, full_square)

    def test_eye(self):
        self.turtle.rotate(0.25 * np.pi)
        self.turtle.forward(np.sqrt(2 * 10**2))

        eye = np.eye(self.size, dtype=self.array.dtype) * self.turtle.color
        npt.assert_array_equal(self.array, eye)
