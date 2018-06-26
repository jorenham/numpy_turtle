import numpy as np
from scipy.misc import toimage

from numpy_turtle import Turtle, l_system


def main():
    """Create the Sierpinski triangle

    https://en.wikipedia.org/wiki/Sierpinski_triangle
    """
    axiom = 'F-G-G'
    rules = {
        'F': 'F-G+F+G-F',
        'G': 'GG',
    }

    angle = 2 * np.pi / 3
    cols = 512
    rows = int(np.ceil(cols * np.sin(angle / 2)))
    n = 8

    a = np.zeros((rows, cols))
    s = l_system.grow(axiom, rules, n)

    t = Turtle(a)
    t.position = rows, 0
    t.rotate(np.pi / 2)

    for s_n in s:
        if s_n == 'F' or s_n == 'G':
            t.forward(cols / 2**n)
        elif s_n == '-':
            t.rotate(angle)
        elif s_n == '+':
            t.rotate(-angle)

    toimage(a).show()


if __name__ == '__main__':
    main()
