from typing import Tuple, Union

import numpy as np
from skimage.draw import line, line_aa

_TAU = np.pi * 2

Color = Union[int, float, Tuple[int, ...], Tuple[float, ...]]


class Turtle:
    def __init__(self, array: np.ndarray, deg: bool = False, aa: bool = False):
        """Draw on a NumPy array using turtle graphics.

        Starts at (0, 0) (top-left corner) with a direction of 0 (pointing
        down).

        Parameters
        ----------
        array: np.ndarray
            The 2D array to write to. Can be either of shape h x w (grayscale),
            h x w x c (e.g. rgb for c=3 channels).
            The dtype is used to determine the color depth of each channel:

              * `bool` for 2 colors.
              * All `np.integer` subtypes for discrete depth, ranging from 0 to
                its max value (e.g. `np.uint8` for values in 0 - 255).
              * All `np.floating` subtypes for continuous depth, ranging from 0
                to 1.

        deg : :obj:`bool`, optional
            Use degrees instead of radians.
        aa : :obj:`bool`, optional
            Enable anti-aliasing.
        """
        if type(array) is not np.ndarray:
            raise TypeError('Array should be a NumPy ndarray')

        self.array = array
        self.aa = aa
        self.deg = deg

        self.__direction = 0
        self.__r, self.__c = 0, 0
        self.__stack = []

        if array.ndim == 2:
            self.__channels = 1
        elif array.ndim == 3:
            self.__channels = array.shape[2]
        else:
            raise TypeError('Array does not have 2 or 3 dimensions')

        if array.dtype == np.dtype(bool):
            self.__depth = 1
            self.__dtype = bool
        elif np.issubdtype(array.dtype, np.integer):
            self.__depth = np.iinfo(array.dtype).max
            self.__dtype = int
        elif np.issubdtype(array.dtype, np.floating):
            self.__depth = 1.0
            self.__dtype = float
        else:
            raise TypeError(
                'Array should have a bool, int-like, or float-like dtype'
            )

        # color initially the max depth (white).
        if self.__channels == 1:
            self.__color = self.__depth
        else:
            self.__color = np.full(self.__channels, self.__depth, self.__dtype)

    def __in_array(self, r=None, c=None):
        r = self.__r if r is None else r
        c = self.__c if c is None else c
        return 0 <= r < self.array.shape[0] and 0 <= c < self.array.shape[1]

    def __clip_coordinate(self, c, axis):
        return min(max(c, 0), self.array.shape[axis] - 1)

    def __draw_line(self, new_c, new_r):
        r0 = int(round(self.__clip_coordinate(self.__r, 0)))
        c0 = int(round(self.__clip_coordinate(self.__c, 1)))
        r1 = int(round(self.__clip_coordinate(new_r, 0)))
        c1 = int(round(self.__clip_coordinate(new_c, 1)))

        if self.aa:
            rr, cc, val = line_aa(r0, c0, r1, c1)
        else:
            rr, cc = line(r0, c0, r1, c1)
            val = 1

        if self.__channels == 1:
            self.array[rr, cc] = val * self.__color
        else:
            for c in range(self.__channels):
                self.array[rr, cc, c] = val * self.__color[c]

    def forward(self, distance: float):
        """Move in the current direction and draw a line with Euclidian
        distance.

        Parameters
        ----------
        distance : int
            The distance to move.
        """

        new_r = self.__r + distance * np.cos(self.__direction)
        new_c = self.__c + distance * np.sin(self.__direction)

        self.__draw_line(int(round(new_c)), int(round(new_r)))

        self.__r = new_r
        self.__c = new_c

    def rotate(self, angle: float):
        """Rotate the turtle by a given angle

        Parameters
        ----------
        angle
            Angle to rotate. Positive rotates left, negative right.
        """
        angle_rad = np.deg2rad(angle) if self.deg else angle
        self.__direction += angle_rad % _TAU

    def push(self):
        """Push the current state (direction and position) to the top of the
        stack.
        """
        self.__stack.append((self.__direction, self.__r, self.__c))

    def pop(self):
        """Restore the state that was last pushed.
        """
        self.__direction, self.__r, self.__c = self.__stack.pop()

    def reset(self):
        """Set direction and position to 0 and empty the stack.
        """
        del self.__stack[:]

    @property
    def direction(self) -> float:
        """float: Get the current direction in radians (or degrees)."""
        return np.rad2deg(self.__direction) if self.deg else self.__direction

    @property
    def position(self) -> Tuple[int, int]:
        """:obj:`tuple` of :obj:`int`: Current row and column position."""
        return self.__r, self.__c

    @position.setter
    def position(self, rc: Tuple[int, int]):
        self.__r, self.__c = rc

    @property
    def color(self) -> Color:
        """int, float, tuple of int or tuple of float: Grayscale color"""
        if self.__channels == 1:
            return self.__color
        else:
            return tuple(self.__color)

    @color.setter
    def color(self, c: Color):
        if not np.isscalar(c) and len(c) != self.__channels:
            raise TypeError('Invalid amount of color values')
        for _c in [c] if np.isscalar(c) else c:
            if _c < 0 or _c > self.__depth:
                raise ValueError('Color value out of range')

        self.__color = np.array(c, dtype=self.__dtype)
