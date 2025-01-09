import math
from pathlib import Path

import numpy as np

import numpy_turtle as np_turtle

AXIOM = "F-F-F-F"
RULES = {
    "F": "FF-F+F-F-FF",
}

COLOR = 180, 80, 0, 255
ANGLE0 = math.tau / 4
ANGLE = math.tau / 4

COLS = 512
ROWS = 512
ITER = 3

OUT = Path(__file__).parent / "images" / (Path(__file__).stem + ".png")


def main() -> None:
    """
    Draw the Sierpinski triangle.

    https://wikipedia.org/wiki/Sierpinski_triangle
    """
    array = np.zeros((ROWS, COLS, len(COLOR)), dtype=np.uint8)
    system = np_turtle.l_system.grow(AXIOM, RULES, ITER)

    turtle = np_turtle.Turtle(array, color=COLOR, aa=False).rotate(ANGLE0)
    turtle.position = ROWS // 2 - 64, COLS - 64

    for s_n in system:
        if s_n in {"F", "G"}:
            turtle.forward(25)
        elif s_n == "-":
            turtle.rotate(ANGLE)
        elif s_n == "+":
            turtle.rotate(-ANGLE)

    turtle.save_image(OUT)


if __name__ == "__main__":
    main()
