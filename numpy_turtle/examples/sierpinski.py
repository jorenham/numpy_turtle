import numpy as np
from scipy.misc import toimage

from numpy_turtle import Turtle

start = 'F-G-G'
rules = {
    'F': 'F-G+F+G-F',
    'G': 'GG',
}
angle = 2 * np.pi / 3
size = 512


def sentence(n):
    s = start

    for _ in range(n):
        s_new = ''
        for s_n in s:
            s_new += rules[s_n] if s_n in rules else s_n
        s = s_new

    return s


def main():
    a = np.zeros((size, size))
    t = Turtle(a)
    n = 8
    s = sentence(n)

    for s_n in s:
        if s_n == 'F' or s_n == 'G':
            t.forward(size / 2**n)
        elif s_n == '-':
            t.rotate(angle)
        elif s_n == '+':
            t.rotate(-angle)

    toimage(a).show()


if __name__ == '__main__':
    main()
