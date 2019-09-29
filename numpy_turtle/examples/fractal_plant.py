import numpy as np
from matplotlib import pyplot as plt
from skimage.io import imsave

from numpy_turtle import Turtle, l_system


def main():
    """Create a fractal plant"""
    axiom = 'X'
    rules = {
        'X': 'F+[[X]-X]-F[-FX]+X',
        'F': 'FF',
    }

    angle = np.pi / 7
    cols, rows = 512, 512
    padding = 32
    n = 6

    a = np.zeros((rows, cols, 4))
    s = l_system.grow(axiom, rules, n)

    t = Turtle(a, aa=True)
    t.position = rows - padding, padding
    t.rotate(np.pi - angle)
    t.color = (0, 1, 0, 1)

    for s_n in s:
        if s_n == 'F':
            t.forward(3)
        elif s_n == '-':
            t.rotate(-angle)
        elif s_n == '+':
            t.rotate(angle)
        elif s_n == '[':
            t.push()
        elif s_n == ']':
            t.pop()

    imsave('images/fractal_plant.png', a)


if __name__ == '__main__':
    main()
