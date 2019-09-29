import numpy as np
from skimage.io import imsave

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

    a = np.zeros((rows, cols, 4))
    s = l_system.grow(axiom, rules, n)

    t = Turtle(a)
    t.position = rows, 0
    t.rotate(np.pi / 2)
    t.color = (0, 0, 0, 1)

    for s_n in s:
        if s_n == 'F' or s_n == 'G':
            t.forward(cols / 2**n)
        elif s_n == '-':
            t.rotate(angle)
        elif s_n == '+':
            t.rotate(-angle)

    imsave('images/sierpinski_triangle.png', a)


if __name__ == '__main__':
    main()
