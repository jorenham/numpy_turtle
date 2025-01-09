from pathlib import Path

import numpy as np

import numpy_turtle as np_turtle

AXIOM = "VZFFF"
RULES = {
    "V": "[+++W][---W]YV",
    "W": "+X[-W]Z",
    "X": "-W[+X]Z",
    "Y": "YZ",
    "Z": "[-FFF][+FFF]F",
}

COLS = 720
ROWS = 666
MARGIN = 64

ANGLE = np.pi / 9
COLOR = 160, 82, 45, 255
ITER = 8

OUT = Path(__file__).parent / "images" / (Path(__file__).stem + ".png")


def main() -> None:
    """Bracketed L-system conifer."""
    array = np.zeros((ROWS, COLS, len(COLOR)), dtype=np.uint8)
    system = np_turtle.l_system.grow(AXIOM, RULES, ITER)

    turtle = np_turtle.Turtle(array, aa=False, color=COLOR).rotate(np.pi)
    turtle.position = ROWS - MARGIN, COLS // 2 - 16

    for s_n in system:
        if s_n.isalpha():
            turtle.forward(14)
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
