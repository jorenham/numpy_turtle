import math
import sys
from collections import deque
from pathlib import Path
from typing import (
    Any,
    Final,
    Generic,
    Literal,
    Self,
    SupportsIndex,
    TypeAlias,
    TypeVar,
    cast,
)

import numpy as np
import numpy.typing as npt
from skimage.draw import line, line_aa  # pyright: ignore[reportUnknownVariableType]
from skimage.io import imsave  # pyright: ignore[reportUnknownVariableType]

_ToColor: TypeAlias = (
    float
    | tuple[float]
    | tuple[float, float, float]
    | tuple[float, float, float, float]
)

_Channels: TypeAlias = Literal[1, 3, 4]

_ScalarT_co = TypeVar(
    "_ScalarT_co",
    bound=np.bool_ | np.integer[Any] | np.floating[Any],
    covariant=True,
)


def _line(
    r0: int,
    c0: int,
    r1: int,
    c1: int,
    *,
    aa: bool = False,
) -> tuple[
    np.ndarray[tuple[int], np.dtype[np.intp]],
    np.ndarray[tuple[int], np.dtype[np.intp]],
    np.ndarray[tuple[int], np.dtype[np.float64]] | int,
]:
    if aa:
        return line_aa(r0, c0, r1, c1)  # pyright: ignore[reportUnknownVariableType]
    return (*line(r0, c0, r1, c1), 1)  # pyright: ignore[reportUnknownVariableType]


class Turtle(Generic[_ScalarT_co]):
    """Draw on a 2-d NumPy array using turtle graphics.

    Starts at (0, 0) (top-left corner) with a direction of 0 (pointing
    down).

    Parameters
    ----------
    array: np.ndarray
        The 2D array to write to. Can be either of shape `(h, w)` (grayscale),
        `(h, w, c)` (RGB for `c=3` channels, or RGBA for `c=4`).
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

    array: Final[npt.NDArray[_ScalarT_co]]
    deg: Final[bool]
    aa: Final[bool]

    _channels: Final[_Channels]
    _depth: Final[float]
    _color: Final[
        np.ndarray[tuple[()], np.dtype[_ScalarT_co]]
        | np.ndarray[tuple[int], np.dtype[_ScalarT_co]]
    ]

    # row, column, direction
    _state: tuple[float, float, float]
    _stack: deque[tuple[float, float, float]]

    def __init__(
        self,
        /,
        array: npt.NDArray[_ScalarT_co],
        *,
        deg: bool = False,
        aa: bool = False,
        color: _ToColor | None = None,
    ) -> None:
        if type(array) is not np.ndarray:
            raise TypeError("Array should be a NumPy ndarray")

        self.array = array
        self.deg = deg
        self.aa = aa

        self._state = 0, 0, 0
        self._stack = deque(maxlen=sys.getrecursionlimit())

        if array.ndim == 2:
            self._channels = 1
        elif array.ndim == 3:
            _, _, c = array.shape
            if c not in {1, 3, 4}:
                raise ValueError("Array should have 1, 3, or 4 channels")
            self._channels = cast("_Channels", c)
        else:
            raise TypeError("Array does not have 2 or 3 dimensions")

        sct = array.dtype.type
        if issubclass(sct, np.bool_):
            self._depth = 1
        elif issubclass(sct, np.integer):
            self._depth = np.iinfo(sct).max
        elif np.issubdtype(array.dtype, np.floating):
            self._depth = 1.0
        else:
            raise TypeError("Array should have a bool, int-like, or float-like dtype")

        if self._channels == 1:
            self._color = np.empty((), sct)
        else:
            self._color = np.empty(self._channels, sct)

        # color initially the max depth on all channels (white).
        self._color[:] = self._depth

        if color is not None:
            self.color = color

    @property
    def position(self, /) -> tuple[float, float]:
        """:obj:`tuple` of :obj:`float`: Current row and column position."""
        return self._state[:2]

    @position.setter
    def position(self, rc: tuple[float, float], /) -> None:
        max_r, max_c, *_ = self.array.shape
        new_r, new_c = rc
        if not (0 <= new_r < max_r) or not (0 <= new_c < max_c):
            raise ValueError("Position out of bounds")

        _, _, d = self._state
        self._state = new_r, new_c, d

    @property
    def direction(self, /) -> float:
        """float: Get the current direction in radians (or degrees)."""
        d = self._state[2]
        return 360 * d / math.tau if self.deg else d

    @property
    def color(self, /) -> float | tuple[float, ...]:
        """int, float, tuple of int or tuple of float: Grayscale color."""
        colorlist = self._color.tolist()
        return tuple(colorlist) if isinstance(colorlist, list) else colorlist

    @color.setter
    def color(self, c: _ToColor, /) -> None:
        if np.size(c) != self._channels:
            raise TypeError("unexpected color channels count")

        c_ = np.array(c, dtype=self.array.dtype)
        if np.any((c_ < 0) | (c_ > self._depth)):
            raise ValueError("Color value out of range")

        assert c_.ndim in {0, 1}
        self._color = c_  # pyright: ignore[reportAttributeAccessIssue]

    def __clip(self, c: float, axis: SupportsIndex) -> int:
        return min(max(round(c), 0), self.array.shape[axis] - 1)

    def __draw(self, new_r: float, new_c: float, /) -> None:
        r, c, _ = self._state
        rr, cc, val = _line(
            self.__clip(r, 0),
            self.__clip(c, 1),
            self.__clip(new_r, 0),
            self.__clip(new_c, 1),
            aa=self.aa,
        )
        self.array[rr, cc] = np.multiply.outer(val, self._color)

    def forward(self, /, distance: float) -> Self:
        """
        Move in the current direction and draw a line with Euclidian distance.

        Parameters
        ----------
        distance : float
            The distance to move.
        """
        r, c, d = self._state
        new_r = r + distance * math.cos(d)
        new_c = c + distance * math.sin(d)

        self.__draw(new_r, new_c)
        self._state = new_r, new_c, d

        return self

    def rotate(self, /, angle: float) -> Self:
        """Rotate the turtle by a given angle.

        If the `Turtle` was created with `deg=False` (default), then the angle must
        be specified in radians. Otherwise, the angle must be specified in degrees.

        Parameters
        ----------
        angle
            Angle to rotate. Positive rotates left, negative right.
        """
        if self.deg:
            if not (-360 < angle < 360):
                raise ValueError("Angle must lie within (-360, 360)")
            dd = angle * math.tau / 360
        else:
            if not (-math.tau < angle < math.tau):
                raise ValueError("Angle must lie within (-2 * pi, 2 * pi)")
            dd = angle

        r, c, d = self._state
        self._state = r, c, (d + dd) % math.tau

        return self

    def push(self, /) -> Self:
        """Push the current state (direction and position) to the top of the stack."""
        self._stack.append(self._state)
        return self

    def pop(self, /) -> Self:
        """Restore the state that was last pushed."""
        self._state = self._stack.pop()
        return self

    def reset(self, /) -> Self:
        """Set direction and position to 0 and empty the stack."""
        self._state = 0, 0, 0
        self._stack.clear()
        return self

    def save_image(self, path: str | Path, /, *, check_contrast: bool = True) -> None:
        """Render the current array to an image and save it to a file."""
        imsave(path, self.array, check_contrast=check_contrast)
