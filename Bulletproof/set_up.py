import math
import random
import numpy as np

import utils
from mod import Mod
from point import Point


def mapToGroup(m, p):
    i = 0
    while i < 256:
        x = utils.hash(utils.concat(m, i))
        rhs = Mod(x, p) ** 3 + 7

        if (Mod(rhs.x, p) ** int((p - 1) / 2)).x == 1:
            y = rhs.squareRoot().x
            if (x, y) != (0, 0):
                return Point(x, y)
        i += 1
    assert False, "Can not map to group"


def computeGenerators(p, g, n):
    h = mapToGroup('string', p)
    i = 0
    gs = np.empty(0)
    hs = np.empty(0)

    while i < n:
        c = random.randint(0, p)
        d = random.randint(0, p)
        gs = np.append(gs, h * c)
        hs = np.append(hs, h * d)
        i = i + 1

    return g, h, gs, hs


def setupRP(g, a, b, p):
    powCheck = True
    i = 0
    while powCheck:
        if 2**i == b:
            powCheck = False
        elif 2**i > 0:
            assert False, "Error: b tiene que ser una potencia de 2."

    n = math.log2(b)
    g, h, gs, hs = computeGenerators(g, n)
