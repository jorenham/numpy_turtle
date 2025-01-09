from pathlib import Path

import numpy as np

import numpy_turtle as np_turtle

AXIOM = "X"
RULES = {
    "X": "F+[[X]-X]-F[-FX]+X",
    "F": "FF",
}

COLS = 666
ROWS = 666
MARGIN = 64

ANGLE = np.pi / 7
COLOR = 0, 255, 0, 255

OUT = Path(__file__).parent / "images" / (Path(__file__).stem + ".png")


def main() -> None:
    """Create a fractal plant."""
    n = 6

    array = np.zeros((ROWS, COLS, len(COLOR)), dtype=np.uint8)
    system = np_turtle.l_system.grow(AXIOM, RULES, n)

    turtle = np_turtle.Turtle(array, aa=True)
    turtle.color = COLOR
    turtle.position = ROWS - MARGIN, MARGIN
    turtle.rotate(np.pi - ANGLE)

    for s_n in system:
        if s_n == "F":
            turtle.forward(4)
        elif s_n == "-":
            turtle.rotate(-ANGLE)
        elif s_n == "+":
            turtle.rotate(ANGLE)
        elif s_n == "[":
            turtle.push()
        elif s_n == "]":
            turtle.pop()

    turtle.save_image(OUT)


if __name__ == "__main__":
    main()
